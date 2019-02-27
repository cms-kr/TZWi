import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

rivetJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("particleLevel:jets"),
    cut = cms.string(""),
    name= cms.string("RivetJet"),
    doc = cms.string("AK4 jets from Rivet-based ParticleLevelProducer"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        # Identical to GenJets, so we just extend their flavor information
        P4Vars,
        hadronFlavour = Var("pdgId", int, doc="PDG id"),
    )
)

rivetNeutrinoTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("particleLevel:neutrinos"),
    cut = cms.string(""),
    name= cms.string("RivetNeutrinos"),
    doc = cms.string("Neutrinos from Rivet-based ParticleLevelProducer"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        # Identical to GenJets, so we just extend their flavor information
        P4Vars,
        pdgId = Var("pdgId", int, doc="PDG id"),
    )
)

