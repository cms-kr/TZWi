import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

def customise_partonTop(process):
    if not hasattr(process, 'partonTop'):
        process.load("TZWi.NanoAODProduction.producers.partonTop_cfi")
        process.nanoAOD_step += process.partonTop

    process.load("TZWi.NanoAODProduction.tables.partonTop_cff")

    process.nanoAOD_step += (
        process.partonTopTable + process.partonTopJetTable
      + process.partonTopChannelTable + process.partonTopJetTable
    )

    return process
