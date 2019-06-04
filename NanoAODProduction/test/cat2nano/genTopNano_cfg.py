import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

process = cms.Process("NANO")
process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.EventContent.EventContent_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "file:/xrootd/store/group/CAT/v8-0-8/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/190407_090210/0000/catTuple_1.root",
    ),
    inputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_catGenTops_*_*',
    ),
)

process.out = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODCATGEN'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('catGenTopNANO.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

process.catGenTopTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("catGenTops"),
    cut = cms.string(""),
    name = cms.string("CatGenTop"),
    doc = cms.string("Generator level top quark and their decay products"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        NJets20 = Var("NJets20", int, doc="Number of Jets"),
        NbJets20 = Var("NbJets20", int, doc="Number of b Jets"),
        NcJets20 = Var("NcJets20", int, doc="Number of c Jets"),
        lepton1_pt = Var("lepton1.pt", float, doc="1st lepton pt"),
        lepton2_pt = Var("lepton2.pt", float, doc="2nd lepton pt"),
        lepton1_eta = Var("lepton1.eta", float, doc="1st lepton eta"),
        lepton2_eta = Var("lepton2.eta", float, doc="2nd lepton eta"),
    )
)

process.p = cms.Path(process.catGenTopTable)
process.outPath = cms.EndPath(process.out)
