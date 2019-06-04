import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

partonTopTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("genTop"),
    cut = cms.string(""),
    name= cms.string("genTop"),
    doc = cms.string("Generator level top quark and their decay products"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False),
    variables = cms.PSet(
        # Identical to GenJets, so we just extend their flavor information
	NJets20 = Var("NJets20", int, doc="Number of Jets"),
        NbJets20 = Var("NbJets20", int, doc="Number of b Jets"),
        NcJets20 = Var("NcJets20", int doc="Number of c Jets"),
        lepton1_pt = Var("lepton1_pt", float, doc="1st lepton pt"),
        lepton2_pt = Var("lepton2_pt", float, doc="2nd lepton pt"),
        lepton1_eta = Var("lepton1_eta", float, doc="1st lepton eta"),
        lepton2_eta = Var("lepton2_eta", float, doc="2nd lepton eta"),
    )
)
