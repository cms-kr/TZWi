import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from ROOT import TLorentzVector
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCMVAinput(Module, object):
    def __init__(self, *args, **kwargs):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        # Basic input variables
        self.out.branch("MVAinput_Status", "i")
        self.out.branch("MVAinput_nGoodJet", "i")
        self.out.branch("MVAinput_WLZL1_dPhi", "F")
        self.out.branch("MVAinput_WLZL1_dR", "F")
        self.out.branch("MVAinput_WLZL2_dPhi", "F")
        self.out.branch("MVAinput_WLZL2_dR", "F")
        self.out.branch("MVAinput_ZL1ZL2_dPhi", "F")
        self.out.branch("MVAinput_ZL1ZL2_dR", "F")
        self.out.branch("MVAinput_Z_mass", "F")
        self.out.branch("MVAinput_W_mass", "F")
        self.out.branch("MVAinput_ZWL_dPhi", "F")
        self.out.branch("MVAinput_ZWL_dR", "F")
        self.out.branch("MVAinput_MET", "F")
        self.out.branch("MVAinput_MET_Phi", "F")
        self.out.branch("MVAinput_TLepton_mass", "F")
        # Inputs for WZCR
        self.out.branch("MVAinput_J1_DeepJetB", "F")
        self.out.branch("MVAinput_J1_pt", "F")
        self.out.branch("MVAinput_ZL1J1_dPhi", "F")
        self.out.branch("MVAinput_ZL1J1_dR", "F")
        self.out.branch("MVAinput_ZL2J1_dPhi", "F")
        self.out.branch("MVAinput_ZL2J1_dR", "F")
        self.out.branch("MVAinput_WLJ1_dPhi", "F")
        self.out.branch("MVAinput_WLJ1_dR", "F")
        # Inputs for TTCR
        self.out.branch("MVAinput_nbJet", "i")
        self.out.branch("MVAinput_bJ_DeepJetB", "F")
        self.out.branch("MVAinput_qJ_DeepJetB", "F")
        self.out.branch("MVAinput_bJ_pt", "F")
        self.out.branch("MVAinput_qJ_pt", "F")
        self.out.branch("MVAinput_bJqJ_dPhi", "F")
        self.out.branch("MVAinput_bJqJ_dR", "F")
        self.out.branch("MVAinput_WLbJ_dPhi", "F")
        self.out.branch("MVAinput_WLbJ_dR", "F")
        self.out.branch("MVAinput_WLqJ_dPhi", "F")
        self.out.branch("MVAinput_WLqJ_dR", "F")
        self.out.branch("MVAinput_ZL1bJ_dPhi", "F")
        self.out.branch("MVAinput_ZL1bJ_dR", "F")
        self.out.branch("MVAinput_ZL1qJ_dPhi", "F")
        self.out.branch("MVAinput_ZL1qJ_dR", "F")
        self.out.branch("MVAinput_ZL2bJ_dPhi", "F")
        self.out.branch("MVAinput_ZL2bJ_dR", "F")
        self.out.branch("MVAinput_ZL2qJ_dPhi", "F")
        self.out.branch("MVAinput_ZL2qJ_dR", "F")
        #self.out.branch("MVAinput_SMTop_mass", "F")
        #self.out.branch("MVAinput_FCNCTop_mass", "F")
        #self.out.branch("MVAinput_TopTop_dEta", "F")
        #self.out.branch("MVAinput_TopTop_dPhi", "F")

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):

        ## initialize ##

        # Just copy from former parts
        self.out.fillBranch("MVAinput_nGoodJet", event._tree.b_out_nGoodJet)
        self.out.fillBranch("MVAinput_Z_mass", event._tree.b_out_Z_mass)
        self.out.fillBranch("MVAinput_W_mass", event._tree.b_out_W_MT)
        self.out.fillBranch("MVAinput_ZWL_dPhi", event._tree.b_out_TriLepton_WleptonZdPhi)
        self.out.fillBranch("MVAinput_ZWL_dR", event._tree.b_out_TriLepton_WleptonZdR)
        self.out.fillBranch("MVAinput_MET", event._tree.b_out_MET_pt)
        self.out.fillBranch("MVAinput_MET_Phi", event._tree.b_out_MET_phi)
        self.out.fillBranch("MVAinput_TLepton_mass", event._tree.b_out_TriLepton_mass)
        self.out.fillBranch("MVAinput_nbJet", event._tree.b_out_nBjet)

        # Basic event selection for WZCR/TTCR
        if ( ( event._tree.b_out_GoodLeptonCode != 111 ) or ( event._tree.b_out_nGoodLepton > 3 ) or ( event._tree.b_out_W_MT > 300 ) ):
            self.out.fillBranch("MVAinput_Status", 0)
            #self.out.fillBranch("MVAinput_nGoodJet", 0)
            self.out.fillBranch("MVAinput_WLZL1_dPhi", 0)
            self.out.fillBranch("MVAinput_WLZL1_dR", 0)
            self.out.fillBranch("MVAinput_WLZL2_dPhi", 0)
            self.out.fillBranch("MVAinput_WLZL2_dR", 0)
            self.out.fillBranch("MVAinput_ZL1ZL2_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1ZL2_dR", 0)
            #self.out.fillBranch("MVAinput_Z_mass", 0)
            #self.out.fillBranch("MVAinput_W_mass", 0)
            #self.out.fillBranch("MVAinput_ZWL_dPhi", 0)
            #self.out.fillBranch("MVAinput_ZWL_dR", 0)
            #self.out.fillBranch("MVAinput_MET", 0)
            #self.out.fillBranch("MVAinput_MET_Phi", 0)
            #self.out.fillBranch("MVAinput_TLepton_mass", 0)
            self.out.fillBranch("MVAinput_J1_DeepJetB", 0)
            self.out.fillBranch("MVAinput_J1_pt", 0)
            self.out.fillBranch("MVAinput_ZL1J1_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1J1_dR", 0)
            self.out.fillBranch("MVAinput_ZL2J1_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2J1_dR", 0)
            self.out.fillBranch("MVAinput_WLJ1_dPhi", 0)
            self.out.fillBranch("MVAinput_WLJ1_dR", 0)
            #self.out.fillBranch("MVAinput_nbJet", 0)
            self.out.fillBranch("MVAinput_bJ_DeepJetB", 0)
            self.out.fillBranch("MVAinput_qJ_DeepJetB", 0)
            self.out.fillBranch("MVAinput_bJ_pt", 0)
            self.out.fillBranch("MVAinput_qJ_pt", 0)
            self.out.fillBranch("MVAinput_bJqJ_dPhi", 0)
            self.out.fillBranch("MVAinput_bJqJ_dR", 0)
            self.out.fillBranch("MVAinput_WLbJ_dPhi", 0)
            self.out.fillBranch("MVAinput_WLqJ_dR", 0)
            self.out.fillBranch("MVAinput_WLbJ_dPhi", 0)
            self.out.fillBranch("MVAinput_WLbJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL1bJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1bJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL1qJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1qJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL2bJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2bJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL2qJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2qJ_dR", 0)
            #self.out.fillBranch("MVAinput_SMTop_mass", 0)
            #self.out.fillBranch("MVAinput_FCNCTop_mass", 0)
            #self.out.fillBranch("MVAinput_TopTop_dEta", 0)
            #self.out.fillBranch("MVAinput_TopTop_dPhi", 0)

            return True
        else:

            # Booking and filling variables for basic variables
            
            Z1Lepton = TLorentzVector()
            Z2Lepton = TLorentzVector()
            WLepton = TLorentzVector()
            ConstZ = TLorentzVector()
            Jet1 = TLorentzVector() # For WZCR
            bJet = TLorentzVector() # For TTCR
            qJet = TLorentzVector() # For TTCR

            WLepton.SetPtEtaPhiM(event._tree.b_out_Lepton1_pt, event._tree.b_out_Lepton1_eta, event._tree.b_out_Lepton1_phi, event._tree.b_out_Lepton1_mass)
            Z1Lepton.SetPtEtaPhiM(event._tree.b_out_Lepton2_pt, event._tree.b_out_Lepton2_eta, event._tree.b_out_Lepton2_phi, event._tree.b_out_Lepton2_mass)
            Z2Lepton.SetPtEtaPhiM(event._tree.b_out_Lepton2_pt, event._tree.b_out_Lepton2_eta, event._tree.b_out_Lepton2_phi, event._tree.b_out_Lepton2_mass)
            ConstZ.SetPtEtaPhiM(event._tree.b_out_Z_pt, event._tree.b_out_Z_eta, event._tree.b_out_Z_phi, event._tree.b_out_Z_mass)
            
            self.out.fillBranch("MVAinput_WLZL1_dPhi", WLepton.DeltaPhi(Z1Lepton))
            self.out.fillBranch("MVAinput_WLZL1_dR", WLepton.DeltaR(Z1Lepton))
            self.out.fillBranch("MVAinput_WLZL2_dPhi", WLepton.DeltaPhi(Z2Lepton))
            self.out.fillBranch("MVAinput_WLZL2_dR", WLepton.DeltaR(Z2Lepton))
            self.out.fillBranch("MVAinput_ZL1ZL2_dPhi", Z1Lepton.DeltaPhi(Z2Lepton))
            self.out.fillBranch("MVAinput_ZL1ZL2_dR", Z1Lepton.DeltaR(Z1Lepton))

            # For WZCR case

            if ( ( abs( ConstZ.M() - 91.2) < 7.5 ) and ( event._tree.b_out_nGoodJet >= 1 ) and\
               ( event._tree.b_out_nBjet == 0 ) and ( event._tree.b_out_LeadingLepton_pt > 25 ) and ( event._tree.b_out_Z_charge == 0 ) ):

                Jet1.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])
                
                self.out.fillBranch("MVAinput_J1_DeepJetB", event._tree.b_out_GoodJet_DeepFlavB[0]) # Should be changed to DeepJet b tagger
                self.out.fillBranch("MVAinput_J1_pt", Jet1.Pt())
                self.out.fillBranch("MVAinput_ZL1J1_dPhi", Z1Lepton.DeltaPhi(Jet1))
                self.out.fillBranch("MVAinput_ZL1J1_dR", Z1Lepton.DeltaR(Jet1))
                self.out.fillBranch("MVAinput_ZL2J1_dPhi", Z2Lepton.DeltaPhi(Jet1))
                self.out.fillBranch("MVAinput_ZL2J1_dR", Z2Lepton.DeltaR(Jet1))
                self.out.fillBranch("MVAinput_WLJ1_dPhi", WLepton.DeltaPhi(Jet1))
                self.out.fillBranch("MVAinput_WLJ1_dR", WLepton.DeltaR(Jet1))
                self.out.fillBranch("MVAinput_Status", 1) # Status flag 1 : WZCR

                return True
            # For TTCR case

            elif ( not( 20 < abs(ConstZ.M() - 91.2) < 60 ) and ( 2 <= event._tree.b_out_nGoodJet <= 3) and\
                    ( event._tree.b_out_nBjet >= 1 ) and ( event._tree.b_out_LeadingLepton_pt > 25 ) and ( event._tree.b_out_Z_charge == 0 ) ):

                BJet = TLorentzVector()
                QJet = TLorentzVector()
                BJet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])
                QJet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[1], event._tree.b_out_GoodJet_eta[1], event._tree.b_out_GoodJet_phi[1], event._tree.b_out_GoodJet_mass[1])
                btagBj = event._tree.b_out_GoodJet_DeepFlavB[0] # Should be changed to DeepJet b tagger
                btagQj = event._tree.b_out_GoodJet_DeepFlavB[1] # Should be changed to DeepJet b tagger

                if ( btagBj < btagQj ):
                    BJet, QJet = QJet, BJet
                    btagBj, btagQj = btagBj, btagQj

                #SMTop = TLorentzVector()
                #FCNCTop = TLorentzVector()
                #SMTop.SetPtEtaPhiM(event._tree.b_out_KinTopWb_pt, event._tree.b_out_KinTopWb_eta, event._tree.b_out_KinTopWb_phi, event._tree.b_out_KinTopWb_mass)
                #FCNCTop.SetPtEtaPhiM(event._tree.b_out_KinTopZq_pt, event._tree.b_out_KinTopZq_eta, event._tree.b_out_KinTopZq_phi, event._tree.b_out_KinTopZq_mass)

                self.out.fillBranch("MVAinput_bJ_DeepJetB", btagBj)
                self.out.fillBranch("MVAinput_qJ_DeepJetB", btagQj)
                self.out.fillBranch("MVAinput_bJ_pt", BJet.Pt())
                self.out.fillBranch("MVAinput_qJ_pt", QJet.Pt())
                self.out.fillBranch("MVAinput_bJqJ_dPhi", BJet.DeltaPhi(QJet))
                self.out.fillBranch("MVAinput_bJqJ_dR", BJet.DeltaR(QJet))
                self.out.fillBranch("MVAinput_WLbJ_dPhi", WLepton.DeltaPhi(BJet))
                self.out.fillBranch("MVAinput_WLbJ_dR", WLepton.DeltaR(BJet))
                self.out.fillBranch("MVAinput_WLqJ_dPhi", WLepton.DeltaPhi(QJet))
                self.out.fillBranch("MVAinput_WLqJ_dR", WLepton.DeltaR(QJet))
                self.out.fillBranch("MVAinput_ZL1bJ_dPhi", Z1Lepton.DeltaPhi(BJet))
                self.out.fillBranch("MVAinput_ZL1bJ_dR", Z1Lepton.DeltaR(BJet))
                self.out.fillBranch("MVAinput_ZL1qJ_dPhi", Z1Lepton.DeltaPhi(QJet))
                self.out.fillBranch("MVAinput_ZL1qJ_dR", Z1Lepton.DeltaR(QJet))
                self.out.fillBranch("MVAinput_ZL2bJ_dPhi", Z2Lepton.DeltaPhi(BJet))
                self.out.fillBranch("MVAinput_ZL2bJ_dR", Z2Lepton.DeltaR(BJet))
                self.out.fillBranch("MVAinput_ZL2qJ_dPhi", Z2Lepton.DeltaPhi(QJet))
                self.out.fillBranch("MVAinput_ZL2qJ_dR", Z2Lepton.DeltaR(QJet))
            # Top varlables not handled at here.
            #    if ( event._tree.b_out_KinTop_status == 1 ): # Check 2 top are reconstructed
            #    self.out.fillBranch("MVAinput_SMTop_mass", SMTop[3])
            #    self.out.fillBranch("MVAinput_FCNCTop_mass", FCNCTop[3])
            #    self.out.fillBranch("MVAinput_TopTop_dEta", abs(SMTop[1] - FCNCTop[1]))
            #    self.out.fillBranch("MVAinput_TopTop_dPhi", abs(SMTop[2] - FCNCTop[2]))
            #    self.out.fillBranch("MVAinput_Status", 2) # Status flag 2 : TTCR
            #    else:
            #        self.out.fillBranch("MVAinput_SMTop_mass", 0)
            #        self.out.fillBranch("MVAinput_FCNCTop_mass", 0)
            #        self.out.fillBranch("MVAinput_TopTop_dEta", 0)
            #        self.out.fillBranch("MVAinput_TopTop_dPhi", 0)
            #        self.out.fillBranch("MVAinput_Status", 3) # Status flag 3 : TTCR but 2 top are not reconstructed

        return True

fcncMVAinput = lambda: FCNCMVAinput()
