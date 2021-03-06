import copy, os, sys

data_path = "/data/rschoefbeck/cmgTuples/Run2015D/hadd/"

SingleMuon_Run2015D_PromptReco = { "name" : "SingleMuon_Run2015D-PromptReco-v3","lumi":204.6}
MuonEG_Run2015D_PromptReco = { "name" : "MuonEG_Run2015D-PromptReco-v3","lumi":209.2}
SingleElectron_Run2015D_PromptReco = { "name" : "SingleElectron_Run2015D-PromptReco-v3","lumi":204.5}
DoubleEG_Run2015D_PromptReco = { "name" : "DoubleEG_Run2015D-PromptReco-v3","lumi":209.2}
DoubleMuon_Run2015D_PromptReco = { "name" : "DoubleMuon_Run2015D-PromptReco-v3","lumi":204.2}
JetHT_Run2015D_PromptReco = { "name" : "JetHT_Run2015D-PromptReco-v3","lumi":205.2}
MET_Run2015D_PromptReco = { "name" : "MET_Run2015D-PromptReco-v3","lumi":209.2}

allSamples_Data25ns = [SingleMuon_Run2015D_PromptReco, MuonEG_Run2015D_PromptReco, SingleElectron_Run2015D_PromptReco, DoubleEG_Run2015D_PromptReco, DoubleMuon_Run2015D_PromptReco, JetHT_Run2015D_PromptReco, MET_Run2015D_PromptReco]

for s in allSamples_Data25ns:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"tree.root",
    "skimAnalyzerDir":"",
    "treeName":"tree",
    'isData':True,
    'dir' : data_path
  })
