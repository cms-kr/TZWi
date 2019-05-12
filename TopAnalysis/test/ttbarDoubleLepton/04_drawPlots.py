#!/usr/bin/env python
from ROOT import *
from glob import glob
import sys, os
import yaml

gROOT.SetBatch(True)
gROOT.LoadMacro("%s/src/PhysicsTools/Utilities/macros/setTDRStyle.C" % os.environ["CMSSW_RELEASE_BASE"])
setTDRStyle()
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

def findPlots(din):
    ret = []
    hists = []
    for dName in [x.GetName() for x in din.GetListOfKeys()]:
        d = din.Get(dName)
        if not d.IsA().InheritsFrom("TDirectory"):
            hists.append(d.GetName())
        else:
            ret.extend(findPlots(din.GetDirectory(dName)))
    if len(hists) > 0: ret.append(din.GetPath().split(':',1)[-1][1:])
    return ret

def buildCanvas(prefix, hists, opt):
    dirname, basename = os.path.dirname(prefix), os.path.basename(prefix)
    lumi = opt['lumi']

    hRDs, hMCs, hNoStacks = hists
    hRD, hMC = None, None
    hsMC = THStack(dirname+"/hsMC"+basename, prefix)
    hsNoStack = THStack(dirname+"/hsNoStack"+basename, prefix) if len(hNoStacks) > 0 else None
    leg = TLegend(0.55, 0.72, 0.93, 0.85)

    for h in hNoStacks:
        leg.AddEntry(h, h.GetTitle(), "l")
    for h in hMCs:
        leg.AddEntry(h, h.GetTitle(), "F")
    leg.AddEntry(hRD, "Data", "lp")

    for h in hRDs:
        if hRD == None:
            hRD = h.Clone()
            hRD.SetName(dirname+"/hRD"+basename)
            hRD.Reset()
        hRD.Add(h)
    for h in reversed(hMCs):
        h.Scale(lumi*1E3)
        if hMC == None:
            hMC = h.Clone()
            hMC.SetName(dirname+"/hMC"+basename)
            hMC.Reset()
        hsMC.Add(h)
        hMC.Add(h)
    for h in reversed(hNoStacks):
        h.Scale(lumi*1E3)
        hsNoStack.Add(h)

    hRatio = hRD.Clone()
    hRatio.SetName(dirname+"/hr"+basename)
    hRatio.Reset()
    hRatio.Divide(hMC, hRD, 1, 1, "B")

    ## Set range
    maxY = max(hMC.GetMaximum(), hRD.GetMaximum())
    if opt['doLogY']:
        #hsMC.SetMinimum(1e-2)
        #hMC.SetMinimum(0.1*min([hMC.GetBinContent(i+1) for i in range(hMC.GetNbinsX()) if hMC.GetBinContent(i+1) > 0]+
        #                       [hRD.GetBinContent(i+1) for i in range(hRD.GetNbinsX()) if hRD.GetBinContent(i+1) > 0]))
        hMC.SetMinimum(0.1*min([hMCs[-1].GetBinContent(i+1) for i in range(hMCs[-1].GetNbinsX()) if hMCs[-1].GetBinContent(i+1) > 0]+
                               [hRD.GetBinContent(i+1) for i in range(hRD.GetNbinsX()) if hRD.GetBinContent(i+1) > 0]))
        hMC.SetMaximum(maxY*pow(10, 1./0.7))
    else:
        hMC.SetMinimum(0)
        hMC.SetMaximum(maxY/0.7)
    hRatio.SetMinimum(0)
    hRatio.SetMaximum(2)

    ## Set titles
    hsMC.SetTitle("%s;%s;%s" % (hsMC.GetTitle(), hMC.GetXaxis().GetTitle(), hMC.GetYaxis().GetTitle()))
    hRatio.SetTitle("MC/Data;;MC/Data")

    ## Set styles
    leg.SetNColumns(3)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)

    hRD.SetMarkerSize(1.)
    hRD.SetMarkerColor(kBlack)
    hRD.SetLineColor(kBlack)
    hRD.SetMarkerStyle(kFullCircle)
    hMC.GetXaxis().SetTitleSize(0.05)
    hMC.GetXaxis().SetTitleOffset(1.20)
    hMC.GetXaxis().SetLabelSize(0.04)
    hMC.GetYaxis().SetTitleSize(0.05)
    hMC.GetYaxis().SetTitleOffset(1.20)
    hMC.GetYaxis().SetLabelSize(0.04)

    hRatio.SetMarkerSize(1.)
    hRatio.SetMarkerColor(kBlack)
    hRatio.SetLineColor(kBlack)
    hRatio.SetMarkerStyle(kFullCircle)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetTitleOffset(0.8)
    hRatio.GetXaxis().SetLabelSize(0.1)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetYaxis().SetLabelSize(0.1)
    hRatio.GetYaxis().SetNdivisions(505)

    ## Draw
    c = TCanvas("c%s" % prefix.replace('/','_'), prefix, 500, 700)
    c.Divide(1,2)

    pad1 = c.cd(1)
    pad1.SetPad(0, 2./7, 1, 1)
    pad1.SetTopMargin(0.1)
    pad1.SetLogy(opt['doLogY'])

    hMC.Draw("hist")
    hsMC.Draw("histsame")
    hRD.Draw("sameLP")
    if hsNoStack != None: hsNoStack.Draw("same,nostack")
    hMC.Draw("axissame")
    leg.Draw()

    pad2 = c.cd(2)
    pad2.SetPad(0, 0, 1, 2./7)
    pad2.SetBottomMargin(0.12)

    hRatio.Draw("ep")

    c.Print("plots/%s/%s/%s.png" % (mode, stepName, hName))
    return c, pad1, pad2, leg, hRD, hMC, hsMC, hsNoStack
    

info = {}
info.update(yaml.load(open("config/plots.yaml")))
info.update(yaml.load(open("config/grouping.yaml")))
info.update(yaml.load(open("config/histogramming.yaml")))

modes = ["ElEl", "MuMu", "MuEl"]
files = []
objs = {}
for mode in modes:
    f = TFile("hist/%s.root" % mode)

    for step in info['steps']:
        stepName = step['name']
        if not os.path.exists("plots/%s/%s" % (mode, stepName)): os.makedirs("plots/%s/%s" % (mode, stepName))
        for hName in step['hists']:
            d = f.Get("%s/h%s" % (stepName, hName))
            hRDs, hMCs, hNoStacks = [], [], []
            for procName, proc in info['processes'].iteritems():
                title = proc['title']
                h = d.Get(title)
                if h == None: continue
                h.AddBinContent(h.GetNbinsX(), h.GetBinContent(h.GetNbinsX()+1))

                ## Apply style
                color = None
                for histStyle in info['histStyles']:
                    if 'title' in histStyle and histStyle['title'] != title: continue
                    if 'color' in histStyle: color = histStyle['color']
                if color != None: h.SetFillColor(eval(color))

                if title.startswith("Data"): hRDs.append(h)
                elif title in info['stackorders']: hMCs.append(h)
                else: hNoStacks.append(h)
            hMCs.sort(key=lambda x : info['stackorders'].index(x.GetName()))

            opt = {}
            opt['lumi'] = sum(info['lumi'])
            opt['doLogY'] = True
            for canvasStyle in info['canvasStyles']:
                if 'substr' in canvasStyle and \
                   not (canvasStyle['substr'] != '' and canvasStyle['substr'] not in mode+'/'+stepName): continue
                if 'logy' in canvasStyle: doLogY = canvasStyle['logy']

            obj = buildCanvas("%s/%s/%s" % (mode, stepName, hName), (hRDs, hMCs, hNoStacks), opt)
            #objs["%s/%s/%s" % (mode, stepName, hName)] = [c]#, hsMC, hMC, hRD, hRatio, leg]

            #obj[0].Print("plots/%s/%s/%s.png" % (mode, stepName, hName))

    files.append(f)

