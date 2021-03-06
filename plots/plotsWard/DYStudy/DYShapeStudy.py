import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()
import numpy

from math import *
from StopsDilepton.tools.helpers import getChain,getWeight,getVarValue
from StopsDilepton.tools.localInfo import *
from datetime import datetime

start = datetime.now()
print '\n','\n', "Starting code",'\n','\n'

#######################################################
#        SELECT WHAT YOU WANT TO DO HERE              #
#######################################################
reduceStat = 1 #recude the statistics, i.e. 10 is ten times less samples to look at
makedraw1D = True

btagcoeff          = 0.89
metcut             = 0.
metsignifcut       = 8.
dphicut            = 0.25
mllcut             = 20
ngoodleptons       = 2
luminosity         = 10000

presel_met         = 'met_pt>'+str(metcut)
presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1'
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_ngoodlep    = '((nGoodMuons+nGoodElectrons)=='+str(ngoodleptons)+')'
presel_OS          = 'isOS'

#preselection: MET>40, njets>=2, n_bjets>=1, n_lep>=2
#For now see here for the Sum$ syntax: https://root.cern.ch/root/html/TTree.html#TTree:Draw@2
preselection = presel_met+'&&'+presel_ngoodlep+'&&'+presel_OS

#######################################################
#                 load all the samples                #
#######################################################
from StopsDilepton.samples.cmgTuples_Spring15_25ns_postProcessed import *
backgrounds = [DY_25ns,DYHT_25ns]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds:
  s['chain'] = getChain(s,histname="")


mt2llbinning = "(10,0,400)"
metbinning = "(10,0,500)"
leadingbinning = "(10,0,1000)"
subleadingbinning = "(10,0,500)"


plots = {\
  'dl_mt2ll':{\
    '_onZ_0b': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_onZ_b==0b', 'binning': mt2llbinning, 'histo':{}},
    '_offZ_0b': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_offZ_b==0b',  'binning': mt2llbinning, 'histo':{}},
    '_onZ_1mb': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_onZ_b>=1',  'binning': mt2llbinning, 'histo':{}},
    '_offZ_1mb': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_offZ_b>=1',  'binning': mt2llbinning, 'histo':{}},
    },
  'met':{\
    '_onZ_0b': {'title':'MET (GeV)', 'name':'MET_onZ_b==0b', 'binning': metbinning, 'histo':{}},
    '_offZ_0b': {'title':'MET (GeV)', 'name':'MET_offZ_b==0b', 'binning': metbinning, 'histo':{}},
    '_onZ_1mb': {'title':'MET (GeV)', 'name':'MET_onZ_b>=1', 'binning': metbinning, 'histo':{}},
    '_offZ_1mb': {'title':'MET (GeV)', 'name':'MET_offZ_b>=1', 'binning': metbinning, 'histo':{}},
    },
  'l1_pt':{\
    '_onZ_0b': {'title':'leading lepton p_T (GeV)', 'name':'Leading_onZ_b==0b', 'binning': leadingbinning, 'histo':{}},
    '_offZ_0b': {'title':'leading lepton p_T (GeV)', 'name':'Leading_offZ_b==0b', 'binning': leadingbinning, 'histo':{}},
    '_onZ_1mb': {'title':'leading lepton p_T (GeV)', 'name':'Leading_onZ_b>=1', 'binning': leadingbinning, 'histo':{}},
    '_offZ_1mb': {'title':'leading lepton p_T (GeV)', 'name':'Leading_offZ_b>=1', 'binning': leadingbinning, 'histo':{}},
    },
  'l2_pt':{\
    '_onZ_0b': {'title':'subleading lepton p_T (GeV)', 'name':'Subleading_onZ_b==0b', 'binning': subleadingbinning, 'histo':{}},
    '_offZ_0b': {'title':'subleading lepton p_T (GeV)', 'name':'Subleading_offZ_b==0b', 'binning': subleadingbinning, 'histo':{}},
    '_onZ_1mb': {'title':'subleading lepton p_T (GeV)', 'name':'Subleading_onZ_b>=1', 'binning': subleadingbinning, 'histo':{}},
    '_offZ_1mb': {'title':'subleading lepton p_T (GeV)', 'name':'Subleading_offZ_b>=1', 'binning': subleadingbinning, 'histo':{}},
    }
  }


#######################################################
#            Start filling in the histograms          #
#######################################################

for s in backgrounds:
  chain = s["chain"]
  for plot in plots.keys():

    if s == DYHT_25ns: preselection += '&&Sum$(Jet_pt)<150'
  
    chain.Draw(plot+">>"+plot+"_onZ_0b"+s["name"]+plots[plot]['_onZ_0b']['binning'],preselection+'&&abs(dl_mass-90.2)<15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0')
    plots[plot]['_onZ_0b']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_onZ_0b"+s["name"])
    
    chain.Draw(plot+">>"+plot+"_offZ_0b"+s["name"]+plots[plot]['_offZ_0b']['binning'],preselection+'&&abs(dl_mass-90.2)>15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0')
    plots[plot]['_offZ_0b']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_offZ_0b"+s["name"])

    chain.Draw(plot+">>"+plot+"_onZ_1mb"+s["name"]+plots[plot]['_onZ_1mb']['binning'],preselection+'&&abs(dl_mass-90.2)<15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1')
    plots[plot]['_onZ_1mb']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_onZ_1mb"+s["name"])

    chain.Draw(plot+">>"+plot+"_offZ_1mb"+s["name"]+plots[plot]['_offZ_1mb']['binning'],preselection+'&&abs(dl_mass-90.2)>15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1')
    plots[plot]['_offZ_1mb']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_offZ_1mb"+s["name"])

    for selection in plots[plot].keys():
      plots[plot][selection]['histo'][s['name']].Sumw2()
      nbinsx= plots[plot][selection]['histo'][s['name']].GetNbinsX()
      lastbin = plots[plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
      overflowbin = plots[plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
      plots[plot][selection]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)


processtime = datetime.now()
print "Time to process chains: ", processtime - start

#######################################################
#             Drawing done here                       #
#######################################################
#Some coloring
DY_25ns["color"]=8
DYHT_25ns["color"]=9

legendtextsize = 0.032

ROOT.gStyle.SetErrorX(0.5)

for i,b in enumerate(backgrounds):
  for plot in plots.keys():

    #Make a stack for backgrounds
    l=ROOT.TLegend(0.5,0.8,0.95,1.0)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.SetTextSize(legendtextsize)

    #Plot!
    c1 = ROOT.TCanvas()

    for j,selection in enumerate(plots[plot].keys()):
      integral = plots[plot][selection]['histo'][b["name"]].Integral()
      plots[plot][selection]['histo'][b["name"]].Scale(1./integral)

      plots[plot][selection]['histo'][b["name"]].SetLineColor(j+1)
      plots[plot][selection]['histo'][b["name"]].SetLineWidth(1)
      plots[plot][selection]['histo'][b["name"]].SetMarkerColor(j+1)
      plots[plot][selection]['histo'][b["name"]].Draw("pe1same")
      if j == 0: 
        plots[plot][selection]['histo'][b["name"]].SetMaximum(3)
        plots[plot][selection]['histo'][b["name"]].SetMinimum(10**-7)
        plots[plot][selection]['histo'][b["name"]].GetXaxis().SetTitle(plots[plot][selection]['title'])
        plots[plot][selection]['histo'][b["name"]].GetYaxis().SetTitle("Events (A.U.)")
      l.AddEntry(plots[plot][selection]['histo'][b["name"]],plots[plot][selection]['name'])
    c1.SetLogy()
    l.Draw()
    c1.Print(plotDir+"/test/DYstudy/"+plot+"_"+s["name"]+".png")

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start
