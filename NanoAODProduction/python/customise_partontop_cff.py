import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

def customise_partontop(process):
    if not hasattr(process, 'partonTop'):
        process.load("TZWi.NanoAODProduction.producers.partonTop_cfi")
        process.nanoAOD_step += process.partonTop

    process.partonTopTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
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
        )
    )

    process.partonTopJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
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

    process.nanoAOD_step += process.partonTopTable
    process.nanoAOD_step += process.partonTopJetTable

    return process
