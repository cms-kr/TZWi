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

def calcError(hist, binstart, binend):
    herr = 0.
    h = hist
    for i in range(binstart, binend):
        herr += (h.GetBinError(i))**2
        sqrterr = math.sqrt(herr)
    return sqrterr

# Error calculation for f=AB or f=A/B
def getRErr(AR, BR, AE, BE, funcType):
    if ( funcType == 0 ):
        func = AR*BR
    else:
        func = AR/BR
    ratA = (AE/AR)**2
    ratB = (BE/BR)**2
    RatioErr = func*(math.sqrt(ratA+ratB))
    return RatioErr

# Error calculation for f=ABC
def getRErr2(AR, BR, CR, AE, BE, CE):
    ratA = (AE/AR)**2
    ratB = (BE/BR)**2
    ratC = (CE/CR)**2
    RatioErr = math.sqrt(ratA+ratB+ratC)
    return RatioErr

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
    hTTrd = f.Get("TTCR/hZ_mass/Data")
    hTTtt = f.Get("TTCR/hZ_mass/ttJets")
    hTTDY = f.Get("TTCR/hZ_mass/DYJets")
    hTTWZ = f.Get("TTCR/hZ_mass/WZ")
    hTTTV = f.Get("TTCR/hZ_mass/ttV")
    hTTSR = f.Get("TTSR/hZ_mass/ttJets")

    hlist = [hWZ, hZZ, hDYJets]

    hnlist = []
    for i,h in enumerate(hlist):
        hnlist.append(h.Integral())

    nWZJets = hnlist[0]
    nZZs = hnlist[1]
    nDYJets = hnlist[2]

    totMC = nWZJets+nZZs+nDYJets
    totData = hrd.Integral()
    rWZ = 35900*nWZJets/totData
    rZZ = 35900*nZZs/totData
    rDY = 35900*nDYJets/totData

    ## For gaussian constraint
    gcent = [rWZ, rZZ, rDY] # Initial ratio before fitting
    #gerr = [0.2, 0.1, 0.1] # gaussian width for constraint fit parameter
    gerr = [rWZ/2, rZZ/2, rDY/2] # gaussian width for constraint fit parameter : for test

    x = RooRealVar("x", "x", 0, 300)

    fWZ = RooRealVar("fWZ", "fWZ", rWZ, 0.0, 0.9)
    fZZ = RooRealVar("fZZ", "fZZ", rZZ, 0.0, 0.9)
    fDY = RooRealVar("fDY", "fDY", rDY, 0.0, 0.9)

    fWZ_cnt = RooGaussian("fWZ_cnt", "fWZ_cnt", fWZ, RooFit.RooConst(rWZ), RooFit.RooConst(gerr[0]))
    fZZ_cnt = RooGaussian("fZZ_cnt", "fZZ_cnt", fZZ, RooFit.RooConst(rZZ), RooFit.RooConst(gerr[1]))
    fDY_cnt = RooGaussian("fDY_cnt", "fDY_cnt", fDY, RooFit.RooConst(rDY), RooFit.RooConst(gerr[2]))

    xArg = RooArgList(x)
    data = RooDataHist("data", "data point with x", xArg, hrd)
    WZ = RooDataHist("WZ", "WZ point with x", xArg, hWZ)
    ZZ = RooDataHist("ZZ", "ZZ point with x", xArg, hZZ)
    DYJets = RooDataHist("DYJets", "DY point with x", xArg, hDYJets)
    WZpdf = RooHistPdf("WZpdf", "WZpdf", RooArgSet(RooArgList(x)), WZ)
    ZZpdf = RooHistPdf("ZZpdf", "ZZpdf", RooArgSet(RooArgList(x)), ZZ)
    DYpdf = RooHistPdf("DYpdf", "DYpdf", RooArgSet(RooArgList(x)), DYJets)

    model = RooAddPdf("model", "model", RooArgList(ZZpdf, DYpdf, WZpdf), RooArgList(fZZ, fDY)) # WZ fix 

    #model.fitTo(data) # Without gaussian constraint
    model.fitTo(data, RooFit.ExternalConstraints(RooArgSet(fZZ_cnt, fDY_cnt))) # With gaussian constraint

    ## Central value
    # WZ fix
    fracZZ = fZZ.getVal()
    fracDY = fDY.getVal()
    fracWZ = 1-fracZZ-fracDY

    fraclist = [fracWZ, fracZZ, fracDY]

    ## Error
    # WZ fix
    errZZ = fZZ.getError()
    errDY = fDY.getError()
    errWZ = math.sqrt(errZZ**2+errDY**2)

    errlist = [errWZ, errZZ, errDY]
 
    cplot = TCanvas("cplot", "cplot", 1)
    xframe = x.frame()
    data.plotOn(xframe)
    model.plotOn(xframe)
    xframe.Draw()
    cplot.SaveAs("fitresult_WZCR_%s.png"%ch)

  # Ratio calculation
    ratio0b = []
    ratio23j = []
    estedlist = []
    ratio0berr = []
    ratio23jerr = []
    ### For temporal calculation ## Should be changed!!
    nrd = hrd.Integral()
    ###

  ### For TTCR
  
    hTTlist = [hTTtt, hTTDY, hTTWZ, hTTTV]

    hTTnlist = []
    for i,h in enumerate(hTTlist):
        hTTnlist.append(h.Integral())

    nTTtt = hTTnlist[0]
    nTTDY = hTTnlist[1]
    nTTWZ = hTTnlist[2]
    nTTTV = hTTnlist[3]

    #totTTMC = nTTtt+nTTDY+nTTWZ+nTTTV
    totTTMC = nTTtt+nTTDY+nTTTV
    totTTData = hTTrd.Integral()
    rTTtt = 35900*nTTtt/totTTData
    rTTDY = 35900*nTTDY/totTTData
    rTTWZ = 35900*nTTWZ/totTTData
    rTTTV = 35900*nTTTV/totTTData

    ## For Gaussian constraint
    TTgcent = [rTTtt, rTTDY, rTTWZ, rTTTV] # Initial ratio before fitting
    #TTgerr = [0.25, 0.1, 0.05, 0.05] # Gaussian width for constraint fit parameter
    TTgerr = [rTTtt/2, rTTDY/2, rTTWZ/2, rTTTV/2] # Gaussian width for constraint fit parameter : for test
 
    y = RooRealVar("y", "y", 30, 150)

    fTTtt = RooRealVar("fTTtt", "fTTtt", rTTtt, 0.0, 0.9)
    fTTDY = RooRealVar("fTTDY", "fTTDY", rTTDY, 0.0, 0.9)
    fTTWZ = RooRealVar("fTTWZ", "fTTWZ", rTTWZ, 0.0, 0.9)
    fTTTV = RooRealVar("fTTTV", "fTTTV", rTTTV, 0.0, 0.9)

    fTTtt_cnt = RooGaussian("fTTtt_cnt", "fTTtt_cnt", fTTtt, RooFit.RooConst(rTTtt), RooFit.RooConst(TTgerr[0]))
    fTTDY_cnt = RooGaussian("fTTDY_cnt", "fTTDY_cnt", fTTDY, RooFit.RooConst(rTTDY), RooFit.RooConst(TTgerr[1]))
    fTTWZ_cnt = RooGaussian("fTTWZ_cnt", "fTTWZ_cnt", fTTWZ, RooFit.RooConst(rTTWZ), RooFit.RooConst(TTgerr[2]))
    fTTTV_cnt = RooGaussian("fTTTV_cnt", "fTTTV_cnt", fTTTV, RooFit.RooConst(rTTTV), RooFit.RooConst(TTgerr[3]))

    yArg = RooArgList(y)
    TTdata = RooDataHist("TTdata", "data point with y", yArg, hTTrd)
    TTtt = RooDataHist("TTtt", "tt point with y", yArg, hTTtt)
    TTDY = RooDataHist("TTDY", "DY point with y", yArg, hTTDY)
    TTWZ = RooDataHist("TTWZ", "WZ point with y", yArg, hTTWZ)
    TTTV = RooDataHist("TTTV", "TTV point with y", yArg, hTTTV)
    TTttpdf = RooHistPdf("TTttpdf", "TTttpdf", RooArgSet(RooArgList(y)), TTtt)
    TTDYpdf = RooHistPdf("TTDYpdf", "TTDYpdf", RooArgSet(RooArgList(y)), TTDY)
    TTWZpdf = RooHistPdf("TTWZpdf", "TTWZpdf", RooArgSet(RooArgList(y)), TTWZ)
    TTTVpdf = RooHistPdf("TTTVpdf", "TTTVpdf", RooArgSet(RooArgList(y)), TTTV)

    Tmodel = RooAddPdf("Tmodel", "Tmodel", RooArgList(TTttpdf, TTDYpdf, TTWZpdf, TTTVpdf), RooArgList(fTTtt, fTTDY, fTTWZ)) # TTjets+DY+TTV+WZ
    #Tmodel = RooAddPdf("Tmodel", "Tmodel", RooArgList(TTttpdf, TTDYpdf, TTWZpdf), RooArgList(fTTtt, fTTDY)) # TTjets+DY+WZ
    #Tmodel = RooAddPdf("Tmodel", "Tmodel", RooArgList(TTttpdf, TTDYpdf, TTTVpdf), RooArgList(fTTtt, fTTDY)) # TTjets+DY+TTV

    #Tmodel.fitTo(TTdata) # Without gaussian constraint
    Tmodel.fitTo(TTdata, RooFit.ExternalConstraints(RooArgSet(fTTtt_cnt, fTTDY_cnt, fTTWZ_cnt)))

    ## Central value
    fracTTtt = fTTtt.getVal()
    #fracTTDY = fTTDY.getVal()
    #fracTTWZ = fTTWZ.getVal()
    #fracTTTV = 1-fracTTtt-fracTTDY-fracTTWZ

    #fracTTlist = [fracTTtt, fracTTDY, fracTTWZ, fracTTTV]

    ## Error
    errTTtt = fTTtt.getError()
    #errTTDY = fTTDY.getError()
    #errTTWZ = fTTWZ.getError()
    #errTTTV = math.sqrt(errTTtt**2+errTTDY**2+errTTWZ**2)

    #errTTlist = [errTTtt, errTTDY, errTTWZ, errTTTV]

    TTcplot = TCanvas("TTcplot", "TTcplot", 1)
    yframe = y.frame()
    TTdata.plotOn(yframe)
    Tmodel.plotOn(yframe)
    yframe.Draw()
    TTcplot.SaveAs("fitresult_TTCR_%s.png"%ch)

    TTdataerr = calcError(hTTrd, hTTrd.FindBin(30), hTTrd.FindBin(150))
    TTerr = getRErr(fracTTtt, totTTData, errTTtt, TTdataerr, 0)
    nttsr = hTTSR.Integral()

    file = open(result, "a")
    wline = "%s TT %f %f %f\n" %(ch, totTTData*fracTTtt*15/80, TTerr*15/80, 35900*nttsr)
    file.write(wline)
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
        n23j0berr = calcError(hista, 3, 5)
        n1j0b = hista.Integral()
        n1j0berr = calcError(hista, 1, 5)
        ratio0b.append(n23j0b/n1j0b)
        ratio0berr.append(getRErr(n23j0b, n1j0b, n23j0berr, n1j0berr, 1))
        n1b23j = histb.Integral(2,2)
        n1b23jerr = calcError(histb, 2, 3)
        n0b23j = histb.Integral(1,1)
        n0b23jerr = calcError(histb, 1, 2)
        ratio23j.append(n1b23j/n0b23j)
        ratio23jerr.append(getRErr(n1b23j, n0b23j, n1b23jerr, n0b23jerr, 1))
        ### Should be changed!!! ###
        estedWZCR = 35900 * totMC * fraclist[i] * ratio0b[i] * ratio23j[i]
        errWZCR = estedWZCR * getRErr2(fraclist[i], ratio0b[i], ratio23j[i], errlist[i], ratio0berr[i], ratio23jerr[i])
        ###
        file = open(result, "a")
        wline = "%s %s %f %f %f %f %f %f %f %f %f %f\n" %(ch, mc, hnlist[i]*35900, 35900*totMC*fraclist[i], 35900*totMC*errlist[i], ratio0b[i], ratio0berr[i], ratio23j[i], ratio23jerr[i], estedWZCR, errWZCR, nexplist[i]*35900)
        file.write(wline)
        file.close()

    f.Close()
