import ROOT
import os
from math import sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag):
        if muonSelectionTag=="TightWP_2016":
            mu_f_BF = ["Mu_Trig_2016BCDEF.root","Mu_ID_2016BCDEF.root","Mu_ISO_2016BCDEF.root"]
            mu_f_GH = ["Mu_Trig_2016GH.root","Mu_ID_2016GH.root","Mu_ISO_2016GH.root"]
            mu_h = ["IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio",
                    "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio",
                    "TightISO_TightID_pt_eta/pt_abseta_ratio"]
        if electronSelectionTag=="TightWP_2016":
            el_f = ["TightWP_2016.root"]
            el_h = ["EGamma_SF2D"]
        mu_f_BF = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_BF]
        mu_f_GH = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_GH]
        el_f = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in el_f]

        mu_f_Trig_BF = [mu_f_BF[0]]
        mu_f_Trig_GH = [mu_f_GH[0]]
        mu_h_Trig = [mu_h[0]]
        mu_f_ID_BF = [mu_f_BF[1]]
        mu_f_ID_GH = [mu_f_GH[1]]
        mu_h_ID = [mu_h[1]]
        mu_f_ISO_BF = [mu_f_BF[2]]
        mu_f_ISO_GH = [mu_f_GH[2]]
        mu_h_ISO = [mu_h[2]]

        self.mu_f_BF = ROOT.std.vector(str)(len(mu_f_BF))
        self.mu_f_GH = ROOT.std.vector(str)(len(mu_f_GH))
        self.mu_h = ROOT.std.vector(str)(len(mu_f_BF))
        for i in range(len(mu_f_BF)): self.mu_f_BF[i] = mu_f_BF[i]; self.mu_h[i] = mu_h[i];
        for i in range(len(mu_f_GH)): self.mu_f_GH[i] = mu_f_GH[i];
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        for i in range(len(el_f)): self.el_f[i] = el_f[i]; self.el_h[i] = el_h[i];

        self.mu_f_Trig_BF = ROOT.std.vector(str)(len(mu_f_Trig_BF))
        self.mu_f_Trig_GH = ROOT.std.vector(str)(len(mu_f_Trig_GH))
        self.mu_h_Trig = ROOT.std.vector(str)(len(mu_f_Trig_BF))
        for i in range(len(mu_f_Trig_BF)): self.mu_f_Trig_BF[i] = mu_f_Trig_BF[i]; self.mu_h_Trig[i] = mu_h_Trig[i];
        for i in range(len(mu_f_Trig_GH)): self.mu_f_Trig_GH[i] = mu_f_Trig_GH[i];
        self.mu_f_ID_BF = ROOT.std.vector(str)(len(mu_f_ID_BF))
        self.mu_f_ID_GH = ROOT.std.vector(str)(len(mu_f_ID_GH))
        self.mu_h_ID = ROOT.std.vector(str)(len(mu_f_ID_BF))
        for i in range(len(mu_f_ID_BF)): self.mu_f_ID_BF[i] = mu_f_ID_BF[i]; self.mu_h_ID[i] = mu_h_ID[i];
        for i in range(len(mu_f_ID_GH)): self.mu_f_ID_GH[i] = mu_f_ID_GH[i];
        self.mu_f_ISO_BF = ROOT.std.vector(str)(len(mu_f_ISO_BF))
        self.mu_f_ISO_GH = ROOT.std.vector(str)(len(mu_f_ISO_GH))
        self.mu_h_ISO = ROOT.std.vector(str)(len(mu_f_ISO_BF))
        for i in range(len(mu_f_ISO_BF)): self.mu_f_ISO_BF[i] = mu_f_ISO_BF[i]; self.mu_h_ISO[i] = mu_h_ISO[i];
        for i in range(len(mu_f_ISO_GH)): self.mu_f_ISO_GH[i] = mu_f_ISO_GH[i];

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/TZWi/TopAnalysis/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker_mu_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_BF,self.mu_h)
        self._worker_mu_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_GH,self.mu_h)
        self._worker_el = ROOT.LeptonEfficiencyCorrector(self.el_f,self.el_h)
        self._worker_muTrig_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_Trig_BF,self.mu_h_Trig)
        self._worker_muTrig_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_Trig_GH,self.mu_h_Trig)
        self._worker_muID_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_BF,self.mu_h_ID)
        self._worker_muID_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_GH,self.mu_h_ID)
        self._worker_muISO_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_BF,self.mu_h_ISO)
        self._worker_muISO_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_GH,self.mu_h_ISO)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LeptonSF", "F")
        self.out.branch("LeptonSFerr", "F")
        self.out.branch("Muon_effSF", "F", lenVar="nMuon")
        self.out.branch("Electron_effSF", "F", lenVar="nElectron")
        self.out.branch("Muon_effSFerr", "F", lenVar="nMuon")
        self.out.branch("Electron_effSFerr", "F", lenVar="nElectron")
        self.out.branch("Muon_effSF_Trig", "F", lenVar="nMuon")
        self.out.branch("Muon_effSFerr_Trig", "F", lenVar="nMuon")
        self.out.branch("Muon_effSF_ID", "F", lenVar="nMuon")
        self.out.branch("Muon_effSFerr_ID", "F", lenVar="nMuon")
        self.out.branch("Muon_effSF_ISO", "F", lenVar="nMuon")
        self.out.branch("Muon_effSFerr_ISO", "F", lenVar="nMuon")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        sf_el = [ self._worker_el.getSF(el.pdgId,el.pt,el.eta) for el in electrons ]
        sf_elerr = [ self._worker_el.getSFErr(el.pdgId,el.pt,el.eta) for el in electrons ]

        sf_mu_BF = [ self._worker_mu_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_GH = [ self._worker_mu_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_BF = [ self._worker_mu_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_GH = [ self._worker_mu_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]

        sf_mu_Trig_BF = [ self._worker_muTrig_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_Trig_GH = [ self._worker_muTrig_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_Trig_BF = [ self._worker_muTrig_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_Trig_GH = [ self._worker_muTrig_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_ID_BF = [ self._worker_muID_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_ID_GH = [ self._worker_muID_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_ID_BF = [ self._worker_muID_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_ID_GH = [ self._worker_muID_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_ISO_BF = [ self._worker_muISO_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_mu_ISO_GH = [ self._worker_muISO_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_ISO_BF = [ self._worker_muISO_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
        sf_muerr_ISO_GH = [ self._worker_muISO_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]

        sf_mu, sf_muerr = [], []
        sf_mu_Trig, sf_muerr_Trig = [], []
        sf_mu_ID, sf_muerr_ID = [], []
        sf_mu_ISO, sf_muerr_ISO = [], []
        for i in range(len(sf_mu_BF)):
            sf_mu.append(0.54778 * sf_mu_BF[i] + 0.45222 * sf_mu_GH[i])
            sf_mu_Trig.append(0.54778 * sf_mu_Trig_BF[i] + 0.45222 * sf_mu_Trig_GH[i])
            sf_mu_ID.append(0.54778 * sf_mu_ID_BF[i] + 0.45222 * sf_mu_ID_GH[i])
            sf_mu_ISO.append(0.54778 * sf_mu_ISO_BF[i] + 0.45222 * sf_mu_ISO_GH[i])
            sf_muerr.append(sqrt(0.54778**2 * sf_muerr_BF[i]**2 + 0.45222**2 * sf_muerr_GH[i]**2))
            sf_muerr_Trig.append(sqrt(0.54778**2 * sf_muerr_Trig_BF[i]**2 + 0.45222**2 * sf_muerr_Trig_GH[i]**2))
            sf_muerr_ID.append(sqrt(0.54778**2 * sf_muerr_ID_BF[i]**2 + 0.45222**2 * sf_muerr_ID_GH[i]**2))
            sf_muerr_ISO.append(sqrt(0.54778**2 * sf_muerr_ISO_BF[i]**2 + 0.45222**2 * sf_muerr_ISO_GH[i]**2))

        eventSFset = sf_el + sf_mu
        eventSFerrset = sf_elerr + sf_muerr
        evsfval = 1.
        evsferrval = 0
        for sfval in eventSFset:
            evsfval *= sfval
        for sferrval in eventSFerrset:
            evsferrval += sferrval**2
	
        self.out.fillBranch("LeptonSF", evsfval)
        self.out.fillBranch("LeptonSFerr", sqrt(evsferrval))
        self.out.fillBranch("Electron_effSF", sf_el)
        self.out.fillBranch("Electron_effSFerr", sf_elerr)
        self.out.fillBranch("Muon_effSF", sf_mu)
        self.out.fillBranch("Muon_effSFerr", sf_muerr)
        self.out.fillBranch("Muon_effSF_Trig", sf_mu_Trig)
        self.out.fillBranch("Muon_effSFerr_Trig", sf_muerr_Trig)
        self.out.fillBranch("Muon_effSF_ID", sf_mu_ID)
        self.out.fillBranch("Muon_effSFerr_ID", sf_muerr_ID)
        self.out.fillBranch("Muon_effSF_ISO", sf_mu_ISO)
        self.out.fillBranch("Muon_effSFerr_ISO", sf_muerr_ISO)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF = lambda : lepSFProducer("TightWP_2016", "TightWP_2016")
