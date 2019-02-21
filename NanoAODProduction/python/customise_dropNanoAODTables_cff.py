import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

def customise_dropNanoAODTables(process):
    for moduleName in process.nanoAOD_step.moduleNames():
        if not moduleName.endswith("Table"): continue
        process.nanoAOD_step.remove(getattr(process, moduleName))
    process.NANOAODSIMoutput.outputCommands.remove('keep edmTriggerResults_*_*_*')

    return process
