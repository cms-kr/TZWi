import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

def customise_partonTop(process):
    if not hasattr(process, 'genTop'):
        process.load("TZWi.NanoAODProduction.producers.genTop_cfi")
        process.nanoAOD_step += process.genTop

    process.load("TZWi.NanoAODProduction.tables.genTop_cff")

    process.nanoAOD_step += (
        process.genTopTable
    )

    return process
