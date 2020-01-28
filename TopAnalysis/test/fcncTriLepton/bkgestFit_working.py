from ROOT import *
import sys, json, os, math
#from sysWeight_cfi import *
from array import array

gROOT.SetBatch(True)
def addLegendCMS():
    #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
    tex2 = TLatex(-20.,50.,"Preliminary")
    tex2.SetNDC()
    tex2.SetTextAlign(12)
    tex2.SetX(0.25)
    tex2.SetY(0.97)
    tex2.SetTextColor(2)
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.05)
    tex2.SetTextSizePixels(24)
    #tex2.Draw()

    return tex2

def make_legend(xmin,ymin,xmax,ymax):
    #leg = TLegend(0.65,0.7, 0.89,0.89)
    leg = TLegend(xmin,ymin,xmax,ymax)
    leg.SetFillColor(0)
    leg.SetLineColor(1)
    leg.SetTextFont(62)
    leg.SetTextSize(0.03)

    leg.SetBorderSize(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetLineColor(0)

    return leg

def calcError(hist):
    herr = 0.
    h = hist
    h.Sumw2()
    for i in range(0,30):
      herr += h.GetBinError(i)
    return herr

name = "bkgEst"
result = "fitresult_%s.txt" % name
baseDir = "./hist_bkgest"
chlist = ["ElElEl", "MuElEl", "ElMuMu", "MuMuMu"]
#chlist = ["MuMuMu"]
mclist = ["WZ", "ZZ", "DYJets"]
#rootFile = "%s/ElElEl.root" % baseDir
if os.path.exists(result): os.system("rm -f %s" % result)

for i, ch in enumerate(chlist):

    rootFile = "%s/%s.root" % (baseDir, ch)
    f = TFile.Open(rootFile)

    # Book hists for WZCR, TTCR
    hWZ = f.Get("WZCR/hW_MT/WZ")
    hZZ = f.Get("WZCR/hW_MT/ZZ")
    hDYJets = f.Get("WZCR/hW_MT/DYJets")
    hrd = f.Get("WZCR/hW_MT/Data")
    hTT_all = f.Get("TTCR_allZ/hZ_mass/ttJets")
    hTTrd = f.Get("TTCR_allZ/hZ_mass/Data")
    hTTSR = f.Get("TTSR/hZ_mass/ttJets")

    hlist = [hWZ, hZZ, hDYJets]

    hnlist = []
    for i,h in enumerate(hlist):
        hnlist.append(h.Integral())

    nWZJets = hnlist[0]
    nZZs = hnlist[1]
    nDYJets = hnlist[2]

    totMC = nWZJets+nZZs+nDYJets
    rWZ = nWZJets/totMC
    rZZ = nZZs/totMC
    rDY = nDYJets/totMC

    print "initial RWZ = ", rWZ
    print "initial RZZ = ", rZZ
    print "initial RDY = ", rDY

    x = RooRealVar("x", "x", 0, 300)

    fWZ = RooRealVar("fWZ", "fWZ", rWZ, 0.0, 0.9)
    fZZ = RooRealVar("fZZ", "fZZ", rZZ, 0.0, 0.9)
    fDY = RooRealVar("fDY", "fDY", rDY, 0.0, 0.9)
    nWZ = RooRealVar("nWZ", "nWZ", nWZJets, nWZJets, nWZJets)
    nZZ = RooRealVar("nZZ", "nZZ", nZZs, nZZs, nZZs)
    nDY = RooRealVar("nDY", "nWZ", nDYJets, nDYJets, nDYJets)
    ntot = RooRealVar("ntot", "ntot", totMC, totMC, totMC)
    k = RooRealVar("k", "Normalization Factor", 1, 0.7, 1.3)
    ktot = RooFormulaVar("ktot", "number of tot event after fitting", "k*ntot", RooArgList(k, ntot))

    xArg = RooArgList(x)
    data = RooDataHist("data", "data point with x", xArg, hrd)
    WZ = RooDataHist("WZ", "WZ point with x", xArg, hWZ)
    ZZ = RooDataHist("ZZ", "ZZ point with x", xArg, hZZ)
    DYJets = RooDataHist("DYJets", "DY point with x", xArg, hDYJets)
    WZpdf = RooHistPdf("WZpdf", "WZpdf", RooArgSet(RooArgList(x)), WZ)
    ZZpdf = RooHistPdf("ZZpdf", "ZZpdf", RooArgSet(RooArgList(x)), ZZ)
    DYpdf = RooHistPdf("DYpdf", "DYpdf", RooArgSet(RooArgList(x)), DYJets)

    model = RooAddPdf("model", "model", RooArgList(ZZpdf, DYpdf, WZpdf), RooArgList(fZZ, fDY)) # WZ  
    #model = RooAddPdf("model", "model", RooArgList(WZpdf, DYpdf, ZZpdf), RooArgList(fWZ, fDY)) # ZZ
    #model = RooAddPdf("model", "model", RooArgList(ZZpdf, WZpdf, DYpdf), RooArgList(fZZ, fWZ)) # DY

    model2 = RooAddPdf("model2", "model2", RooArgList(model), RooArgList(ktot))
    model2.fitTo(data)
    k.Print()
    #fWZ.Print()
    fZZ.Print()
    fDY.Print()

    fracZZ = fZZ.getVal()
    fracDY = fDY.getVal()
    fracWZ = 1-fracZZ-fracDY
    fitk = k.getVal()

    fraclist = [fracWZ, fracZZ, fracDY]

    cplot = TCanvas("cplot", "cplot", 1)
    xframe = x.frame()
    data.plotOn(xframe)
    model.plotOn(xframe)
    #WZ.plotOn(xframe, RooFit.LineColor(2), RooFit.LineStyle(9), RooFit.Rescale(fracWZ))
    #DYJets.plotOn(xframe, RooFit.LineColor(3), RooFit.LineStyle(9), RooFit.Rescale(fracWZ))
    xframe.Draw()
    cplot.SaveAs("fitresult_WZCR_%s.png"%ch)

    #entriesWZ = WZpdf.getAnalyticalIntegral(RooArgSet(xArg), RooArgSet(xArg))
    #entriesZZ = ZZpdf.getAnalyticalIntegral(RooArgSet(xArg), RooArgSet(xArg))
    #entriesDY = DYpdf.getAnalyticalIntegral(RooArgSet(xArg), RooArgSet(xArg))

    #print "WZ after fit is = ", 36500*entriesWZ
    #print "ZZ after fit is = ", 36500*entriesZZ
    #print "DY after fit is = ", 36500*entriesDY

    # Ratio calculation
    ratio0b = []
    ratio23j = []
    estedlist = []
    ### For temporal calculation ## Should be changed!!
    nrd = hrd.Integral()
    ###

### For TTCR
    y = RooRealVar("y", "y", 30, 150)
    coef1 = RooRealVar("a", "a", -0.1, 0.1)
  
    yArg = RooArgList(y)
    k1 = RooRealVar("k1", "k1", 0, -0.1, 0.1)
    TTdata = RooDataHist("TTdata", "Data point with x", yArg, hTTrd)
    TT = RooDataHist("TT", "TT point with x", yArg, hTT_all)
    linmodel = RooPolynomial("linmodel", "linmodel", y, RooArgList(coef1)) # Model for linear check

    ## Save Linear check result
    linmodel.fitTo(TT)
    coef1.Print()
    x1 = coef1.getVal()
    file = open(result, "a")
    lline = "Linear check TTCR %s %f\n" %(ch, x1)
    file.write(lline)
    file.close()

    tcplot = TCanvas("tcplot", "tcplot", 1)
    yframe = y.frame()
    TT.plotOn(yframe)
    linmodel.plotOn(yframe)
    yframe.Draw()
    tcplot.SaveAs("LinearCheck_TTCR_%s.png"%ch)

    ## Save TTCR fit Result

    nttsr = hTTSR.Integral()
    errttsr = calcError(hTTSR)

    linmodel.fitTo(TTdata, RooFit.Range(30, 70))
    coef1.Print()
    ttplot = TCanvas("ttplot", "ttplot", 1)
    tframe = y.frame()
    TTdata.plotOn(tframe)
    linmodel.plotOn(tframe)
    #tframe.Draw()
    t1 = coef1.getVal()
    linmodel.fitTo(TTdata, RooFit.Range(110, 150))
    coef1.Print()
    linmodel.plotOn(tframe)
    tframe.Draw()
    t2 = coef1.getVal()
    ttplot.SaveAs("fitresult_TTCR_%s.png"%ch)
    t11 = hTT_all.Integral(30, 70)
    t22 = hTT_all.Integral(110, 150) 
    file = open(result, "a")
    tline = "%s TT %f %f\n"%(ch, 15*(abs(t1)+abs(t2)), 35900*nttsr)
    #tline = "%s TT %f %f\n"%(ch, 36500*(t11+t22)*15/80, 36500*nttsr)
    file.write(tline)
    file.close()

### To extract expected entries
    hexpWZ = f.Get("TTSR/hW_MT/WZ")
    hexpZZ = f.Get("TTSR/hW_MT/ZZ")
    hexpDY = f.Get("TTSR/hW_MT/DYJets")
    hexplist = [hexpWZ, hexpZZ, hexpDY]

    nexplist = []
    for i,h in enumerate(hexplist):
        nexplist.append(h.Integral())
    
    for i, mc in enumerate(mclist):
        hista = f.Get("WZCR_0b/hnGoodJet/%s" % mc)    
        histb = f.Get("WZCR_23jet/hnBjet/%s" % mc)
        n23j0b = hista.Integral(3,4)
        n1j0b = hista.Integral()
        ratio0b.append(n23j0b/n1j0b)
        n1b23j = histb.Integral(2,2)
        n0b23j = histb.Integral(1,1)
        ratio23j.append(n1b23j/n0b23j)
        ### Should be changed!!! ###
        estedWZCR = 35900 * totMC * fitk * fraclist[i] * ratio0b[i] * ratio23j[i]
        ###

        file = open(result, "a")
        wline = "%s %s %f %f %f %f %f %f\n" %(ch, mc, hnlist[i]*35900, 35900*totMC*fitk*fraclist[i], ratio0b[i], ratio23j[i], estedWZCR, nexplist[i]*35900)
        file.write(wline)
        file.close()

    f.Close()
