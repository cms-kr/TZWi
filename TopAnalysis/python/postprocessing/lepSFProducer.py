import ROOT
import os
from math import sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag, mode):
        if muonSelectionTag=="TightWP_2016":
            mu_f_BF = ["Mu_ID_2016BCDEF.root","Mu_ISO_2016BCDEF.root"]
            mu_f_GH = ["Mu_ID_2016GH.root","Mu_ISO_2016GH.root"]
            mu_h = ["MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio",
                    "TightISO_TightID_pt_eta/pt_abseta_ratio"]
        if electronSelectionTag=="TightWP_2016":
            el_f = ["TightWP_2016.root"]
            el_h = ["EGamma_SF2D"]
        if mode=="ElElEl":
            self.TrigSF = [0.9026, 0.9392, 1.0032, 1.0366]
        elif mode=="MuElEl":
            self.TrigSF = [0.9665, 0.9498, 1.0307, 1.0472]
        elif mode=="ElMuMu":
            self.TrigSF = [0.9785, 0.9714, 0.8809, 1.0669]
        elif mode=="MuMuMu":
            self.TrigSF = [1.0022, 1.0023, 1.0012, 1.0041]
        else:
            self.TrigSF = [1., 1., 1., 1.]
        mu_f_BF = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_BF]
        mu_f_GH = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_GH]
        el_f = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in el_f]

        mu_f_ID_BF = [mu_f_BF[0]]
        mu_f_ID_GH = [mu_f_GH[0]]
        mu_h_ID = [mu_h[0]]
        mu_f_ISO_BF = [mu_f_BF[1]]
        mu_f_ISO_GH = [mu_f_GH[1]]
        mu_h_ISO = [mu_h[1]]

        self.mu_f_BF = ROOT.std.vector(str)(len(mu_f_BF))
        self.mu_f_GH = ROOT.std.vector(str)(len(mu_f_GH))
        self.mu_h = ROOT.std.vector(str)(len(mu_f_BF))
        for i in range(len(mu_f_BF)): self.mu_f_BF[i] = mu_f_BF[i]; self.mu_h[i] = mu_h[i];
        for i in range(len(mu_f_GH)): self.mu_f_GH[i] = mu_f_GH[i];
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        for i in range(len(el_f)): self.el_f[i] = el_f[i]; self.el_h[i] = el_h[i];

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
        self._worker_muID_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_BF,self.mu_h_ID)
        self._worker_muID_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_GH,self.mu_h_ID)
        self._worker_muISO_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_BF,self.mu_h_ISO)
        self._worker_muISO_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_GH,self.mu_h_ISO)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Lepton_SF", "F")
        self.out.branch("Lepton_SFerr", "F")
        self.out.branch("Electron_SF", "F")
        self.out.branch("Electron_SFerr", "F")
        self.out.branch("Muon_SF", "F")
        self.out.branch("Muon_SFerr", "F")
        self.out.branch("MuonID_SF", "F")
        self.out.branch("MuonID_SFerr", "F")
        self.out.branch("MuonISO_SF", "F")
        self.out.branch("MuonISO_SFerr", "F")
        self.out.branch("Trigger_SF", "F")
        #self.out.branch("Trigger_SFerr", "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")

        sf_el, sf_elerr = [], []
        sf_mu_BF, sf_muerr_BF = [], []
        sf_mu_GH, sf_muerr_GH = [], []
        sf_mu_ID_BF, sf_muerr_ID_BF = [], []
        sf_mu_ID_GH, sf_muerr_ID_GH = [], []
        sf_mu_ISO_BF, sf_muerr_ISO_BF = [], []
        sf_mu_ISO_GH, sf_muerr_ISO_GH = [], []
        el_pt, mu_pt = [], []

        for el in electrons:
            if el.pt < 20 or abs(el.eta) > 2.4 : continue
            if abs(el.eta + el.deltaEtaSC) > 1.4442 and abs(el.eta + el.deltaEtaSC) < 1.566 : continue
            if el.cutBased_Sum16 != 4 : continue
   
            sf_el.append(self._worker_el.getSF(el.pdgId,el.pt,el.eta+el.deltaEtaSC))
            sf_elerr.append(self._worker_el.getSFErr(el.pdgId,el.pt,el.eta+el.deltaEtaSC))

            el_pt.append(el.pt)

        for mu in muons:
            if mu.pt < 20 or abs(mu.eta) > 2.4 : continue
            if mu.tightId == 0 : continue
            if mu.pfRelIso04_all > 0.15 : continue

            sf_mu_BF.append(self._worker_mu_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_GH.append(self._worker_mu_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_BF.append(self._worker_mu_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_GH.append(self._worker_mu_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))

            sf_mu_ID_BF.append(self._worker_muID_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ID_GH.append(self._worker_muID_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ID_BF.append(self._worker_muID_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ID_GH.append(self._worker_muID_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ISO_BF.append(self._worker_muISO_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ISO_GH.append(self._worker_muISO_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ISO_BF.append(self._worker_muISO_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ISO_GH.append(self._worker_muISO_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))

            mu_pt.append(mu.pt)
    
#        sf_el = [ self._worker_el.getSF(el.pdgId,el.pt,el.eta+el.deltaEtaSC) for el in electrons ]
#        sf_elerr = [ self._worker_el.getSFErr(el.pdgId,el.pt,el.eta+el.deltaEtaSC) for el in electrons ]
#
#        sf_mu_BF = [ self._worker_mu_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_GH = [ self._worker_mu_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_BF = [ self._worker_mu_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_GH = [ self._worker_mu_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#
#        sf_mu_ID_BF = [ self._worker_muID_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ID_GH = [ self._worker_muID_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ID_BF = [ self._worker_muID_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ID_GH = [ self._worker_muID_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ISO_BF = [ self._worker_muISO_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ISO_GH = [ self._worker_muISO_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ISO_BF = [ self._worker_muISO_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ISO_GH = [ self._worker_muISO_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#
#        el_pt = [ el.pt for el in electrons ]
#        mu_pt = [ mu.pt for mu in muons ]

        Leadinglep_pt = max(el_pt + mu_pt)
        if Leadinglep_pt >= 0 and Leadinglep_pt < 100 : sf_Trig = self.TrigSF[0]
        elif Leadinglep_pt >= 100 and Leadinglep_pt < 200 : sf_Trig = self.TrigSF[1]
        elif Leadinglep_pt >= 200 and Leadinglep_pt < 300 : sf_Trig = self.TrigSF[2]
        elif Leadinglep_pt >= 300 : sf_Trig = self.TrigSF[3]
        else : sf_Trig = 1

        sf_mu, sf_muerr = [], []
        sf_mu_ID, sf_muerr_ID = [], []
        sf_mu_ISO, sf_muerr_ISO = [], []
        for i in range(len(sf_mu_BF)):
            sf_mu.append(0.54778 * sf_mu_BF[i] + 0.45222 * sf_mu_GH[i])
            sf_mu_ID.append(0.54778 * sf_mu_ID_BF[i] + 0.45222 * sf_mu_ID_GH[i])
            sf_mu_ISO.append(0.54778 * sf_mu_ISO_BF[i] + 0.45222 * sf_mu_ISO_GH[i])
            sf_muerr.append(sqrt(0.54778**2 * sf_muerr_BF[i]**2 + 0.45222**2 * sf_muerr_GH[i]**2))
            sf_muerr_ID.append(sqrt(0.54778**2 * sf_muerr_ID_BF[i]**2 + 0.45222**2 * sf_muerr_ID_GH[i]**2))
            sf_muerr_ISO.append(sqrt(0.54778**2 * sf_muerr_ISO_BF[i]**2 + 0.45222**2 * sf_muerr_ISO_GH[i]**2))

        leptonSFset = sf_el + sf_mu
        leptonSFerrset = sf_elerr + sf_muerr
        leptonSFval = 1.
        leptonSFerrval = 0
        for sfval in leptonSFset:
            leptonSFval *= sfval
        for sferrval in leptonSFerrset:
            leptonSFerrval += sferrval**2

        elSFval = 1.
        elSFerrval = 0
        for sfval in sf_el:
            elSFval *= sfval
        for sferrval in sf_elerr:
            elSFerrval += sferrval**2

        if elSFerrval > 1:
            print elSFerrval, sf_elerr

        muonSFval = 1.
        muonSFerrval = 0
        for sfval in sf_mu:
            muonSFval *= sfval
        for sferrval in sf_muerr:
            muonSFerrval += sferrval**2

        muonIDSFval = 1.
        muonIDSFerrval = 0
        for sfval in sf_mu_ID:
            muonIDSFval *= sfval
        for sferrval in sf_muerr_ID:
            muonIDSFerrval += sferrval**2

        muonISOSFval = 1.
        muonISOSFerrval = 0
        for sfval in sf_mu_ISO:
            muonISOSFval *= sfval
        for sferrval in sf_muerr_ISO:
            muonISOSFerrval += sferrval**2
	
        self.out.fillBranch("Lepton_SF", leptonSFval)
        self.out.fillBranch("Lepton_SFerr", sqrt(leptonSFerrval))
        self.out.fillBranch("Electron_SF", elSFval)
        self.out.fillBranch("Electron_SFerr", sqrt(elSFerrval))
        self.out.fillBranch("Muon_SF", muonSFval)
        self.out.fillBranch("Muon_SFerr", sqrt(muonSFerrval))
        self.out.fillBranch("MuonID_SF", muonIDSFval)
        self.out.fillBranch("MuonID_SFerr", sqrt(muonIDSFerrval))
        self.out.fillBranch("MuonISO_SF", muonISOSFval)
        self.out.fillBranch("MuonISO_SFerr", sqrt(muonISOSFerrval))
        self.out.fillBranch("Trigger_SF", sf_Trig)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF_ElElEl = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "ElElEl")
lepSF_MuElEl = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "MuElEl")
lepSF_ElMuMu = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "ElMuMu")
lepSF_MuMuMu = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "MuMuMu")
