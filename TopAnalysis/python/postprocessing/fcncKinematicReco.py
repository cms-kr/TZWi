import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from ROOT import TLorentzVector
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCKinematicReco(Module, object):
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.get("mode")
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("KinTopWb_pt", "F")
        self.out.branch("KinTopWb_eta", "F")
        self.out.branch("KinTopWb_phi", "F")
        self.out.branch("KinTopWb_mass", "F")
        self.out.branch("KinTopZq_pt", "F")
        self.out.branch("KinTopZq_eta", "F")
        self.out.branch("KinTopZq_phi", "F")
        self.out.branch("KinTopZq_mass", "F")
        self.out.branch("KinTop_status", "i")

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def getKinVar(self, pt, eta, phi, mass):
        KinVar = []
        px = pt*(math.cos(phi))
        py = pt*(math.sin(phi))
        pz = pt*(math.sinh(eta))
        epart = math.sqrt(px*px+py*py+pz*pz+mass*mass) ##
        KinVar = [px, py, pz, epart]
        return KinVar

    def getSol(self, plx, ply, plz, El, lmass, pnx, pny, Wmass):
        possolu = 0
        negsolu = 0
        constflag = 1
        A = 2*(plx*pnx+ply*pny)+(Wmass*Wmass)-(lmass*lmass)
        B = (4*(El*El)*(pnx*pnx+pny*pny))-(A*A)
        aterm = A*plz
        bterm = A*A*plz*plz
        cterm = El*El-plz*plz
        if ( bterm - B*cterm > 0 ):
            possolu = (aterm + math.sqrt(bterm-B*cterm))/(2*cterm)
            negsolu = (aterm - math.sqrt(bterm-B*cterm))/(2*cterm)
            constflag = 1
        else:
            possolu = 0
            negsolu = 0
            constflag = 0
        solu = [possolu, negsolu, constflag]
        #solu = [possolu, negsolu, constflag, A, B, aterm, bterm, cterm] # For debugging
        return solu
    def getTPEPM(self, pxs, pys, pzs, Es):
        sumpx = 0
        sumpy = 0
        sumpz = 0
        sumE = 0
        for i, valx in enumerate(pxs):
            sumpx += valx
        for i, valy in enumerate(pys):
            sumpy += valy
        for i, valz in enumerate(pzs):
            sumpz += valz
        for i, valE in enumerate(Es):
            sumE += valE
        TPt = math.sqrt(sumpx*sumpx+sumpy*sumpy)
        TPhi = math.atan2(sumpy,sumpx) # atan2(y,x)
        TEta = math.asinh(sumpz/TPt)
        TMass = math.sqrt((sumE*sumE)-(sumpx*sumpx)-(sumpy*sumpy)-(sumpz*sumpz))
        TKinVar = [TPt, TEta, TPhi, TMass]
        #TKinVar = [TPt, TEta, TPhi, TMass, sumpx, sumpy, sumpz, sumE] # For debugging
        return TKinVar

    def analyze(self, event):
        Wmass = 80.4 # Fixed W mass
        OriginTmass = 172.5 # Fixed T mass

        ## initialize ##
        SMTKinVal = [0,0,0,0]
        FCNCTKinVal = [0,0,0,0]
        consted = 0

        # For NPL Selecton
        NPLflag = 1
        if 'NPL' in self.mode:
            if (event._tree.b_out_nGoodLepton != 2 and event._tree.b_out_nVetoLepton > 0):
                NPLflag = 0
            else: NPLflag = 1
        else:
            if (event._tree.b_out_nGoodLepton != 3):
                NPLflag = 0
            else: NPLflag = 1

        # Check basic event selection
        if event._tree.b_out_GoodLeptonCode != 111 or\
           not( 2 <= event._tree.b_out_nGoodJet <= 3 ) or\
           event._tree.b_out_nBjet < 1 or\
           NPLflag == 0:

            self.out.fillBranch("KinTop_status", 0)
            self.out.fillBranch("KinTopWb_pt", 0)
            self.out.fillBranch("KinTopWb_eta", 0)
            self.out.fillBranch("KinTopWb_phi", 0)
            self.out.fillBranch("KinTopWb_mass", 0)
            self.out.fillBranch("KinTopZq_pt", 0)
            self.out.fillBranch("KinTopZq_eta", 0)
            self.out.fillBranch("KinTopZq_phi", 0)
            self.out.fillBranch("KinTopZq_mass", 0)

            return True
        else:
            # Variable construct : Lepton vars = [pt, eta, phi, mass]
            Wlepvar = TLorentzVector()
            Zlep1var = TLorentzVector()
            Zlep2var = TLorentzVector()
            Wlepvar.SetPtEtaPhiM(event._tree.b_out_Lepton1_pt, event._tree.b_out_Lepton1_eta, event._tree.b_out_Lepton1_phi, event._tree.b_out_Lepton1_mass)
            Zlep1var.SetPtEtaPhiM(event._tree.b_out_Lepton2_pt, event._tree.b_out_Lepton2_eta, event._tree.b_out_Lepton2_phi, event._tree.b_out_Lepton2_mass)
            Zlep2var.SetPtEtaPhiM(event._tree.b_out_Lepton3_pt, event._tree.b_out_Lepton3_eta, event._tree.b_out_Lepton3_phi, event._tree.b_out_Lepton3_mass)
            # Variable coonstruct : Jet vars = [pt, eta, phi, mass, CSVv2]
            #if event._tree._b_out_nGoodJet < 2: continue # nJet >= 2 for tZq reconstruction
            bvar = TLorentzVector()
            qvar = TLorentzVector()
            bvar.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])
            qvar.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[1], event._tree.b_out_GoodJet_eta[1], event._tree.b_out_GoodJet_phi[1], event._tree.b_out_GoodJet_mass[1])
            #bjetCSV, qjetCSV = event._tree.b_out_GoodJet_CSVv2[0], event._tree.b_out_GoodJet_CSVv2[1]
            bjetDeepFlavB, qjetDeepFlavB = event._tree.b_out_GoodJet_DeepFlavB[0], event._tree.b_out_GoodJet_DeepFlavB[1]
            # Variable condtruct : Neutrino vars = [MET, phi]
            metvar = TLorentzVector()
            metvar.SetPtEtaPhiM(event._tree.b_out_MET_pt, 0, event._tree.b_out_MET_phi, 0)

            ## b jet assign by CSVv2 discriminator
            #if ( bjetCSV < qjetCSV ):
            #    bvar, qvar = qvar, bvar
            #    bjetCSV, qjetCSV = qjetCSV, bjetCSV

            # b jet assign by CSVv2 discriminator
            if ( bjetDeepFlavB < qjetDeepFlavB ):
                bvar, qvar = qvar, bvar
                bjetDeepFlavB, qjetDeepFlavB = qjetDeepFlavB, bjetDeepFlavB

            # pxyzE calculation & construction : [px, py, pz, E]
            Zlep1 = self.getKinVar(Zlep1var.Pt(), Zlep1var.Eta(), Zlep1var.Phi(), 0.)
            Zlep2 = self.getKinVar(Zlep2var.Pt(), Zlep2var.Eta(), Zlep2var.Phi(), 0.)
            Wlep = self.getKinVar(Wlepvar.Pt(), Wlepvar.Eta(), Wlepvar.Phi(), 0.) ## Assume lepton mass = 0
            bjet = self.getKinVar(bvar.Pt(), bvar.Eta(), bvar.Phi(), bvar.M())
            qjet = self.getKinVar(qvar.Pt(), qvar.Eta(), qvar.Phi(), qvar.M())

            # MET pxy calculation & construction : [px, py]
            metpx = metvar.Pt()*(math.cos(metvar.Phi()))
            metpy = metvar.Pt()*(math.sin(metvar.Phi()))
            met = [metpx, metpy]

            # Calculate pz_neu and E_neu
            metpz = self.getSol(Wlep[0], Wlep[1], Wlep[2], Wlep[3], 0., met[0], met[1], Wmass) # Assume lepton mass = 0
            posneuE = math.sqrt((metpx*metpx)+(metpy*metpy)+(metpz[0]*metpz[0]))
            negneuE = math.sqrt((metpx*metpx)+(metpy*metpy)+(metpz[1]*metpz[1]))
            consted = metpz[2] # Reconstructed flag

            # SM Top mass construction
            SMpxs = [bjet[0], Wlep[0], met[0]]
            SMpys = [bjet[1], Wlep[1], met[1]]
            posSMpzs = [bjet[2], Wlep[2], metpz[0]]
            negSMpzs = [bjet[2], Wlep[2], metpz[1]]
            posSMEs= [bjet[3], Wlep[3], posneuE]
            negSMEs= [bjet[3], Wlep[3], negneuE]

            posTMass = self.getTPEPM(SMpxs, SMpys, posSMpzs, posSMEs)[3]
            negTMass = self.getTPEPM(SMpxs, SMpys, negSMpzs, negSMEs)[3]

            ## Top mass variance comparison and reconsruct SM Top KinVals
            if ( math.fabs(posTMass - OriginTmass) < math.fabs(negTMass - OriginTmass) ):
                SMTMass = posTMass
                SMTKinVal = self.getTPEPM(SMpxs, SMpys, posSMpzs, posSMEs)
            else:
                SMTMass = negTMass
                SMTKinVal = self.getTPEPM(SMpxs, SMpys, negSMpzs, negSMEs)

            # FCNC Top reconstruction
            FCNCpxs = [qjet[0], Zlep1[0], Zlep2[0]]
            FCNCpys = [qjet[1], Zlep1[1], Zlep2[1]]
            FCNCpzs = [qjet[2], Zlep1[2], Zlep2[2]]
            FCNCEs = [qjet[3], Zlep1[3], Zlep2[3]]
            FCNCTKinVal = self.getTPEPM(FCNCpxs, FCNCpys, FCNCpzs, FCNCEs)

            self.out.fillBranch("KinTop_status", consted)
            self.out.fillBranch("KinTopWb_pt", SMTKinVal[0])
            self.out.fillBranch("KinTopWb_eta", SMTKinVal[1])
            self.out.fillBranch("KinTopWb_phi", SMTKinVal[2])
            self.out.fillBranch("KinTopWb_mass", SMTKinVal[3])
            self.out.fillBranch("KinTopZq_pt", FCNCTKinVal[0])
            self.out.fillBranch("KinTopZq_eta", FCNCTKinVal[1])
            self.out.fillBranch("KinTopZq_phi", FCNCTKinVal[2])
            self.out.fillBranch("KinTopZq_mass", FCNCTKinVal[3])

        ## for debugging
        #print " Coefficients A/B/aterm/bterm/cterm : ", metpz[3], metpz[4], metpz[5], metpz[6], metpz[7]
        #print " Sum pxyzE for top solution : ", SMTKinVal[4], SMTKinVal[5], SMTKinVal[6], SMTKinVal[7]
        #print "Z lepton 1 : ", Zlep1
        #print "Z lepton 2 : ", Zlep2
        #print "W lepton 1 : ", Wlep
        #print "b jet : ", bjet
        #print "q jet : ", qjet
        #print "neu px, py : ", met 
        #print " Neu Z pos/neg solution : ", metpz[0], metpz[1]
        #print "neu pos/neg energy : ", posneuE, negneuE

        return True

fcncKinReco_ElElEl = lambda: FCNCKinematicReco(mode="ElElEl")
fcncKinReco_ElMuMu = lambda: FCNCKinematicReco(mode="ElMuMu")
fcncKinReco_MuElEl = lambda: FCNCKinematicReco(mode="MuElEl")
fcncKinReco_MuMuMu = lambda: FCNCKinematicReco(mode="MuMuMu")
fcncKinReco_NPLElElEl = lambda: FCNCKinematicReco(mode="NPLElElEl")
fcncKinReco_NPLElMuMu = lambda: FCNCKinematicReco(mode="NPLElMuMu")
fcncKinReco_NPLMuElEl = lambda: FCNCKinematicReco(mode="NPLMuElEl")
fcncKinReco_NPLMuMuMu = lambda: FCNCKinematicReco(mode="NPLMuMuMu")
