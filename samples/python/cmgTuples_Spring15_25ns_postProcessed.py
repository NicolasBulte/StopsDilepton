import copy, os, sys
from StopsDilepton.tools.localInfo import dataDir
import ROOT
dir = dataDir 
#"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",

DoubleEG_25ns={\
"name": "DoubleEG",
"bins": ["DoubleEG_Run2015D-PromptReco-v3/"],
'dir' : dir,
'color': ROOT.kBlack,
}

DoubleMuon_25ns={\
"name": "DoubleMuon",
"bins": ["DoubleMuon_Run2015D-PromptReco-v3/"],
'dir':dir,
'color': ROOT.kBlack,
}

MuonEG_25ns={\
"name": "MuonEG",
"bins": ["MuonEG_Run2015D-PromptReco-v3/"],
'dir':dir,
'color': ROOT.kBlack,
}

TTJets_inclusive_25ns={\
"name" : "tt+Jets",
"bins" : ["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/"],
'dir' : dir,
'color': 7,
}

TTLep_25ns={\
"name" : "tt+Jets2L2Nu",
"dir": dir,
"bins" : ["TTTo2L2Nu_13TeV-powheg_RunII_Spring15DR74-Asympt25ns_MCRUN2_74_V9-v1"],
'color': 7,
}

WJetsHTToLNu_25ns={\
"name" : "W+Jets HT binned",
"bins" : [
"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
#"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
],
'dir' : dir,
'color': ROOT.kRed-10,
}
WJetsToLNu_25ns={\
"name" : "W+Jets",
"bins" : [
"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1"
],
'dir' : dir,
'color': ROOT.kRed-10,
}
diBosons_25ns={\
"name" : "WW+WZ+ZZ",
"bins" : [
"WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
],
'dir' : dir,
'color': ROOT.kOrange,
}

TTX_25ns={\
"name": "TTX",
"bins": [
"TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2"
],
'dir' :dir,
'color': ROOT.kPink,
}

singleTop_25ns={\
"name" : "singletop",
"bins" : [
"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' : dir,
'color': 40,
}
DY_25ns={\
"name" : "DY",
"bins" : [
"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3"
],
'dir' : dataDir,
'color': 8,
}
DYHT_25ns={\
"name" : "DY_HT",
"bins" : [
"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' : dataDir,
'color': 8,
}
DYM10to50_25ns={\
"name" : "DY M10-50",
"bins" : [
"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' : dataDir,
'color': 8,
}
QCDMu_25ns={\
"name" : "QCD_Mu",
"bins" : [
"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2"
],
'dir' : dir,
'color': 46,
}


QCDEle_25ns={\
"name" : "QCD_Ele",
"bins" : [
"QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
],
'dir' : dir,
'color': 46,
}


TTW_25ns={\
"name": "TTW",
"bins": [
"TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' :dir,
'color': ROOT.kYellow,
}

TTZ_QQ_25ns={\
"name": "TTZ_QQ",
"bins": [
"TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' :dir,
'color': 7,
}

TTZ_Lep_25ns={\
"name": "TTZ_LLorNuNu",
"bins": [
"TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' :dir,
'color': 7,
}

TTZ_All_25ns={\
"name": "TTZ",
"bins": [
"TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' :dir,
'color': 7,
}

TTH_25ns={\
"name": "TTH",
"bins": [
"ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2"
],
'dir' :dir,
'color': 16,
}
