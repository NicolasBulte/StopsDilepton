import ROOT
import sys, os, copy, random, subprocess, datetime, shutil
from array import array
from StopsDilepton.tools.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from math import *
from StopsDilepton.tools.mt2Calculator import mt2Calculator 
mt2Calc = mt2Calculator()
from StopsDilepton.tools.mtautau import mtautau as mtautau_
from StopsDilepton.tools.helpers import getChain, getChunks, getObjDict, getEList, getVarValue
from StopsDilepton.tools.objectSelection import getLeptons, getMuons, getElectrons, getGoodMuons, getGoodElectrons, getGoodLeptons, getJets, getGoodBJets, getGoodJets, isBJet 

from StopsDilepton.tools.localInfo import *

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

#from StopsDilepton.samples.xsec import xsec

target_lumi = 1000 #pb-1 Which lumi to normalize to

defSampleStr = "MuonEG_Run2015B_PromptReco"  #Which samples to run for by default (will be overritten by --samples option)

subDir = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/postProcessed_mAODv2" #Output directory -> The first path should go to localInfo (e.g. 'dataPath' or something)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allSamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--inputTreeName", dest="inputTreeName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default=subDir, type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="dilep", type="string", action="store", help="any skim condition?")
parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
parser.add_option("--overwrite", dest="overwrite", default = False, action="store_true", help="Overwrite?")

(options, args) = parser.parse_args()
#assert options.skim.lower() in ['inclusive', 'dilep'], "Unknown skim: %s"%options.skim
skimCond = "(1)"

from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2 import *
if options.skim.lower().startswith("dilep"):
  from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l import *
elif options.skim.lower().startswith("inclusive"):
  from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_0l import *


if options.skim.lower().startswith('dilep'):
  skimCond += "&&Sum$(LepGood_pt>20&&abs(LepGood_eta)<2.5)>=2"

if sys.argv[0].count('ipython'):
  options.small=False

def getTreeFromChunk(c, skimCond, iSplit, nSplit):
  if not c.has_key('file'):return
  rf = ROOT.TFile.Open(c['file'])
  assert not rf.IsZombie()
  rf.cd()
  tc = rf.Get("tree")
  nTot = tc.GetEntries()
  fromFrac = iSplit/float(nSplit)
  toFrac   = (iSplit+1)/float(nSplit)
  start = int(fromFrac*nTot)
  stop  = int(toFrac*nTot)
  ROOT.gDirectory.cd('PyROOT:/')
  print "Copy tree from source: total number of events found:",nTot,"Split counter: ",iSplit,"<",nSplit,"first Event:",start,"nEvents:",stop-start
  t = tc.CopyTree(skimCond,"",stop-start,start)
  tc.Delete()
  del tc
  rf.Close()
  del rf
  return t
   
maxN = 1 if options.small else -1
exec('allSamples=['+options.allSamples+']')
chunks, sumWeight = [], 0.

allData = False not in [s.isData for s in allSamples]
allMC   =  True not in [s.isData for s in allSamples]

assert allData or len(set([s.xSection for s in allSamples]))==1, "Not all samples have the same xSection: %s !"%(",".join([s.name for s in allSamples]))
assert allMC or len(allSamples)==1, "Don't concatenate data samples"

assert False not in [hasattr(s, 'path') for s in allSamples], "Not all samples have a path: "+", ".join([s.name for s in allSamples])

sample=allSamples[0]
if len(allSamples)>1:
  sample.name=sample.name+'_comb'  

outDir = os.path.join(options.targetDir, options.skim, sample.name)
if os.path.exists(outDir) and any([True for f in os.listdir(outDir) if f.endswith('.root')]) and not options.overwrite:
  print "Found non-empty directory: %s -> skipping!"%outDir
  sys.exit(0)
else:
  tmpDir = os.path.join(outDir,'tmp')
  if os.path.exists(outDir): shutil.rmtree(outDir)
  os.makedirs(outDir)
  os.makedirs(tmpDir)

for iSample, sample in enumerate(allSamples):
  tchunks, tsumWeight = getChunks(sample, maxN=maxN)
  chunks+=tchunks; sumWeight += tsumWeight
  print "Now %i chunks from sample %s with sumWeight now %f"%(len(chunks), sample.name, sumWeight)

if options.skim.lower().count('tiny'):
  #branches to be kept for data and MC
  branchKeepStrings_DATAMC = ["run", "lumi", "evt", "isData", "nVert", 
                       "met_pt", "met_phi",
                       "puppiMet_pt","puppiMet_phi",  
                       "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter", "Flag_goodVertices", "Flag_CSCTightHaloFilter", "Flag_eeBadScFilter",
                       "HLT_mumuIso", "HLT_ee_DZ", "HLT_mue"
                       'LepGood_eta','LepGood_pt','LepGood_phi', 'LepGood_dxy', 'LepGood_dz','LepGood_tightId', 'LepGood_pdgId', 'LepGood_mediumMuonId', 'LepGood_miniRelIso', 'LepGood_sip3d', 'LepGood_mvaIdSpring15', 'LepGood_convVeto', 'LepGood_lostHits',
                       'Jet_eta','Jet_pt','Jet_phi','Jet_btagCSV', 'Jet_id' ,
#                       "nLepGood", "LepGood_*", 
#                       "nTauGood", "TauGood_*",
                       ] 

  #branches to be kept for MC samples only
  branchKeepStrings_MC = [ "nTrueInt", "genWeight", "xsec", "puWeight", "met_genPt", "met_genPhi", 
  #                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
  #                     "ngenLep", "genLep_*", 
  #                     "nGenPart", "GenPart_*",
  #                     "ngenPartAll","genPartAll_*","ngenLep","genLep_*"
  #                     "ngenTau", "genTau_*", 
  #                     "ngenLepFromTau", "genLepFromTau_*"
                        ]

  #branches to be kept for data only
  branchKeepStrings_DATA = [
              ]

else:
  #branches to be kept for data and MC
  branchKeepStrings_DATAMC = ["run", "lumi", "evt", "isData", "rho", "nVert", 
  #                     "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40", 
  #                     "nLepGood20", "nLepGood15", "nLepGood10", "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25", 
                       "met_pt", "met_phi","met_Jet*", "met_Unclustered*", "met_sumEt", "met_rawPt", "met_rawSumEt",
                       "metNoHF_pt", "metNoHF_phi",
                       "puppiMet_pt","puppiMet_phi","puppiMet_sumEt","puppiMet_rawPt","puppiMet_rawPhi","puppiMet_rawSumEt",
                       "Flag_*","HLT_*",
  #                     "nFatJet","FatJet_*", 
                       "nJet", "Jet_*", 
                       "nLepGood", "LepGood_*", 
  #                     "nLepOther", "LepOther_*", 
                       "nTauGood", "TauGood_*",
                       ] 

  #branches to be kept for MC samples only
  branchKeepStrings_MC = [ "nTrueInt", "genWeight", "xsec", "puWeight", "met_gen*", 
  #                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
  #                     "ngenLep", "genLep_*", 
  #                     "nGenPart", "GenPart_*",
                       "ngenPartAll","genPartAll_*","ngenLep","genLep_*"
  #                     "ngenTau", "genTau_*", 
  #                     "ngenLepFromTau", "genLepFromTau_*"
                        ]

  #branches to be kept for data only
  branchKeepStrings_DATA = [
              ]

if sample.isData: 
  lumiScaleFactor=1
  branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA 
  jetMCInfo = []
  from FWCore.PythonUtilities.LumiList import LumiList
  sample.lumiList = LumiList(os.path.expandvars(sample.json))
  outputLumiList = {}
  print "Loaded json %s"%sample.json
else:
  lumiScaleFactor = sample.xSection*target_lumi/float(sumWeight)
  branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC
  jetMCInfo = ['mcMatchFlav/I', 'partonId/I']

readVariables = ['met_pt/F', 'met_phi/F', 'run/I', 'lumi/I']
newVariables = ['weight/F']
aliases = [ "met:met_pt", "metPhi:met_phi"]
readVectors = [\
  {'prefix':'LepGood',  'nMax':8, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'charge/I', 'relIso03/F', 'tightId/I', 'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I', 'mvaIdSpring15/F','lostHits/I', 'convVeto/I', 'dxy/F', 'dz/F']},
  {'prefix':'Jet',  'nMax':100, 'vars':['pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'btagCMVA/F'] + jetMCInfo},
]
if not sample.isData: 
  aliases.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
if options.skim.lower().startswith('dilep'):
  newVariables.extend( ['nGoodMuons/I', 'nGoodElectrons/I' ] )
  newVariables.extend( ['dl_pt/F', 'dl_eta/F', 'dl_phi/F', 'dl_mass/F' ] )
  newVariables.extend( ['dl_mt2ll/F', 'dl_mt2bb/F', 'dl_mt2blbl/F', 'dl_mtautau/F', 'dl_alpha0/F',  'dl_alpha1/F' ] )
  newVariables.extend( ['l1_pt/F', 'l1_eta/F', 'l1_phi/F', 'l1_mass/F', 'l1_pdgId/I', 'l1_index/I' ] )
  newVariables.extend( ['l2_pt/F', 'l2_eta/F', 'l2_phi/F', 'l2_mass/F', 'l2_pdgId/I', 'l2_index/I' ] )
  newVariables.extend( ['isEE/I', 'isMuMu/I', 'isEMu/I', 'isOS/I' ] )

newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]

readVars = [readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
for v in readVectors:
  readVars.append(readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
  v['vars'] = [readVar(v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']]

printHeader("Compiling class to write")
writeClassName = "ClassToWrite"#+str(isample)
writeClassString = createClassString(className=writeClassName, vars= newVars, vectors=[], nameKey = 'stage2Name', typeKey = 'stage2Type')
#  print writeClassString
s = compileClass(className=writeClassName, classString=writeClassString, tmpDir='/tmp/')

readClassName = "ClassToRead"#+str(isample)
readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', typeKey = 'stage1Type', stdVectors=False)
printHeader("Class to Read")
#  print readClassString
r = compileClass(className=readClassName, classString=readClassString, tmpDir='/tmp/')

filesForHadd=[]
if options.small: chunks=chunks[:1]
#print "CHUNKS:" , chunks
for chunk in chunks:
  sourceFileSize = os.path.getsize(chunk['file'])
  nSplit = 1+int(sourceFileSize/(200*10**6)) #split into 200MB
  if nSplit>1: print "Chunk too large, will split into",nSplit,"of appox 200MB"
  for iSplit in range(nSplit):
    t = getTreeFromChunk(chunk, skimCond, iSplit, nSplit)
    if not t: 
      print "Tree object not found:", t
      continue
    t.SetName("Events")
    nEvents = t.GetEntries()
    for v in newVars:
#        print "new VAR:" , v
      v['branch'] = t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
    for v in readVars:
#        print "read VAR:" , v
      t.SetBranchAddress(v['stage1Name'], ROOT.AddressOf(r, v['stage1Name']))
    for v in readVectors:
      for var in v['vars']:
        t.SetBranchAddress(var['stage1Name'], ROOT.AddressOf(r, var['stage1Name']))
    for a in aliases:
      t.SetAlias(*(a.split(":")))
    print "File: %s Chunk: %s nEvents: %i (skim: %s) condition: %s lumiScaleFactor: %f"%(chunk['file'],chunk['name'], nEvents, options.skim, skimCond, lumiScaleFactor)
    
    for i in range(nEvents):
      if (i%10000 == 0) and i>0 :
        print i,"/",nEvents  , "name:" , chunk['name']
      s.init()
      r.init()
      t.GetEntry(i)

      genWeight = 1 if sample.isData else t.GetLeaf('genWeight').GetValue()
      s.weight = lumiScaleFactor*genWeight if not sample.isData else 1
      if sample.isData: 
        if not sample.lumiList.contains(r.run, r.lumi):
  #        print "Did not find run %i lumi %i in json file %s"%(r.run, r.lumi, sample.json)
          s.weight=0
        else:
          if r.run not in outputLumiList.keys():
            outputLumiList[r.run] = [r.lumi]
          else:
            if r.lumi not in outputLumiList[r.run]:
              outputLumiList[r.run].append(r.lumi)
#        print "Found run %i lumi %i in json file %s"%(r.run, r.lumi, sample.json)
      if options.skim.lower().startswith('dilep'):
        leptons = getGoodLeptons(r)
        s.nGoodMuons      = len(filter( lambda l:abs(l['pdgId'])==13, leptons))
        s.nGoodElectrons  = len(filter( lambda l:abs(l['pdgId'])==11, leptons))
#          print "Leptons", leptons 
        if len(leptons)>=2:# and leptons[0]['pdgId']*leptons[1]['pdgId']<0 and abs(leptons[0]['pdgId'])==abs(leptons[1]['pdgId']): #OSSF choice
          mt2Calc.reset()
          s.l1_pt  = leptons[0]['pt'] 
          s.l1_eta = leptons[0]['eta']
          s.l1_phi = leptons[0]['phi']
          s.l1_mass   = leptons[0]['mass']
          s.l1_pdgId  = leptons[0]['pdgId']
          s.l1_index  = leptons[0]['index']
          s.l2_pt  = leptons[1]['pt'] 
          s.l2_eta = leptons[1]['eta']
          s.l2_phi = leptons[1]['phi']
          s.l2_mass   = leptons[1]['mass']
          s.l2_pdgId  = leptons[1]['pdgId']
          s.l2_index  = leptons[1]['index']

          l_pdgs = [abs(leptons[0]['pdgId']), abs(leptons[1]['pdgId'])]
          l_pdgs.sort()
          s.isMuMu = l_pdgs==[13,13] 
          s.isEE = l_pdgs==[11,11] 
          s.isEMu = l_pdgs==[11,13] 
          s.isOS = s.l1_pdgId*s.l2_pdgId<0

          l1 = ROOT.TLorentzVector()
          l1.SetPtEtaPhiM(leptons[0]['pt'], leptons[0]['eta'], leptons[0]['phi'], 0 )
          l2 = ROOT.TLorentzVector()
          l2.SetPtEtaPhiM(leptons[1]['pt'], leptons[1]['eta'], leptons[1]['phi'], 0 )
          dl = l1+l2
          s.dl_pt  = dl.Pt()
          s.dl_eta = dl.Eta()
          s.dl_phi = dl.Phi()
          s.dl_mass   = dl.M() 
          mt2Calc.setMet(r.met_pt,r.met_phi)
          mt2Calc.setLeptons(s.l1_pt, s.l1_eta, s.l1_phi, s.l2_pt, s.l2_eta, s.l2_phi)
          s.dl_mt2ll = mt2Calc.mt2ll()
          s.dl_mtautau, s.dl_alpha0, s.dl_alpha1 = mtautau_(r.met_pt,r.met_phi, s.l1_pt, s.l1_eta, s.l1_phi, s.l2_pt, s.l2_eta, s.l2_phi, retAll=True)

          jets = getGoodJets(r)
          if len(jets)>=2:
            bJets = filter(lambda j:isBJet(j), jets)
            nonBJets = filter(lambda j:not isBJet(j), jets)
            bj0, bj1 = (bJets+nonBJets)[:2]
            mt2Calc.setBJets(bj0['pt'], bj0['eta'], bj0['phi'], bj1['pt'], bj1['eta'], bj1['phi'])
            s.dl_mt2bb   = mt2Calc.mt2bb()
            s.dl_mt2blbl = mt2Calc.mt2blbl()
#              print len(bJets), len(nonBJets), s.dl_mt2bb, s.dl_mt2blbl

      for v in newVars:
        v['branch'].Fill()
    newFileName = sample.name+'_'+chunk['name']+'_'+str(iSplit)+'.root'
    filesForHadd.append(newFileName)
    if not options.small:
      f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
      t.SetBranchStatus("*",0)
      for b in branchKeepStrings + [v['stage2Name'] for v in newVars] +  [v.split(':')[1] for v in aliases]:
        t.SetBranchStatus(b, 1)
      t2 = t.CloneTree()
      t2.Write()
      f.Close()
      print "Written",tmpDir+'/'+newFileName
      del f
      del t2
      t.Delete()
      del t
    for v in newVars:
      del v['branch']

print "Event loop end"

if not options.small: 
  size=0
  counter=0
  files=[]
  for f in filesForHadd:
    size+=os.path.getsize(tmpDir+'/'+f)
    files.append(f)
    if size>(0.5*(10**9)) or f==filesForHadd[-1] or len(files)>300:
      ofile = outDir+'/'+sample.name+'_'+str(counter)+'.root'
      print "Running hadd on", tmpDir, files
      os.system('cd '+tmpDir+';hadd -f '+ofile+' '+' '.join(files))
      print "Written output file %s" % ofile
      size=0
      counter+=1
      files=[]
  shutil.rmtree(tmpDir)
  if allData:
    jsonFile = outDir+'/'+sample.name+'.json'
    LumiList(runsAndLumis = outputLumiList).writeJSON(jsonFile)
    print "Written JSON file %s" % jsonFile
