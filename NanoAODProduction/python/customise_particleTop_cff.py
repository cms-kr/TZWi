import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *

def customise_particletop(process):
    if not hasattr(process, 'particleLevel'):
        process.load("PhysicsTools.NanoAOD.particlelevel_cff")

    process.genParticles2HepMC.signalParticlePdgIds = [6, -6]

    process.load("TZWi.NanoAODProduction.tables.particleTop_cff")
    process.rivetLeptonTable.name = "RivetLepton" ## We change the name, default was GenDressedLepton
    
    if process.rivetLeptonTable not in process.nanoAOD_step.moduleNames():
        process.nanoAOD_step += process.rivetLeptonTable
    process.nanoAOD_step += process.rivetJetTable
    process.nanoAOD_step += process.rivetNeutrinoTable

    return process
