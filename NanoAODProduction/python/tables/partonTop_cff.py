import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

partonTopTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("partonTop"),
    cut = cms.string(""),
    name= cms.string("PartonTop"),
    doc = cms.string("Parton level top quark and their decay products"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        # Identical to GenJets, so we just extend their flavor information
        P4Vars,
        pdgId = Var("pdgId", int, doc="PDG id"),
        partonTopIdxMother = Var("?numberOfMothers>0?motherRef(0).key():-1", int, doc="index of the mother particle"),
    )
)

partonTopJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("partonTop:qcdJets"),
    cut = cms.string(""),
    name= cms.string("PartonTopJets"),
    doc = cms.string("Parton level QCD jets"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        # Identical to GenJets, so we just extend their flavor information
        P4Vars,
        pdgId = Var("pdgId", int, doc="PDG id"),
    )
)

partonTopChannelTable = cms.EDProducer("GlobalVariablesTableProducer",
    variables = cms.PSet(
        PartonTopChannel = ExtVar( cms.InputTag("partonTop:channel"), "int", doc = "ttbar parton level channel")
    )
)

partonTopModesTable = cms.EDProducer("IntArrayTableProducer",
    name = cms.string("PartonTopModes"),
    doc = cms.string("Parton level boson decay modes"),
    src = cms.InputTag("partonTop:modes"),
)
