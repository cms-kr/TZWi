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
    lumi = opt['lumi']*1E3

    hRDs, hMCs, hNoStacks = hists
    hRD, hMC = None, None
    hsMC = THStack(dirname+"/hsMC"+basename, prefix)
    hsNoStack = THStack(dirname+"/hsNoStack"+basename, prefix) if len(hNoStacks) > 0 else None
    leg = TLegend(0.50, 0.72, 0.90, 0.85)

    for h in hRDs:
        if hRD == None:
            hRD = h.Clone()
            hRD.SetName(dirname+"/hRD"+basename)
            hRD.Reset()
        hRD.Add(h)
    for h in reversed(hMCs):
        h.Scale(lumi)
        if hMC == None:
            hMC = h.Clone()
            hMC.SetName(dirname+"/hMC"+basename)
            hMC.Reset()
        hsMC.Add(h)
        hMC.Add(h)
    for h in reversed(hNoStacks):
        h.Scale(lumi)
        hsNoStack.Add(h)

    for h in hNoStacks:
        leg.AddEntry(h, h.GetTitle(), "l")
    for h in hMCs:
        leg.AddEntry(h, h.GetTitle(), "F")
    leg.AddEntry(hRD, "Data", "lp")

    hToDraw = hMC if hMC != None else hRD if hRD != None else None

    hRatio = hToDraw.Clone() if hToDraw != None else None
    if hRatio != None:
        hRatio.SetName(dirname+"/hr"+basename)
        hRatio.Reset()
        if None not in (hMC, hRD): hRatio.Divide(hMC, hRD, 1, 1, "B")

    ## Set range
    maxY = max(hMC.GetMaximum() if hMC != None else 0,
               hRD.GetMaximum() if hRD != None else 0)

    if hToDraw != None:
        if opt['doLogY'] and maxY != 0:
            mins = [maxY]
            if hRD != None: mins.extend([hRD.GetBinContent(i+1) for i in range(hRD.GetNbinsX()) if hRD.GetBinContent(i+1) > 0])
            if len(hMCs) != 0: mins.extend([hMCs[-1].GetBinContent(i+1) for i in range(hMCs[-1].GetNbinsX()) if hMCs[-1].GetBinContent(i+1) > 0])
            hToDraw.SetMinimum(0.5*min(mins))

            hToDraw.SetMaximum(maxY*pow(10, 1./0.6))
        else:
            hToDraw.SetMinimum(0)
            hToDraw.SetMaximum(maxY/0.6)
    if hRatio != None:
        hRatio.SetMinimum(0)
        hRatio.SetMaximum(2)

    ## Set titles
    if hMC != None: hsMC.SetTitle("%s;%s;%s" % (hsMC.GetTitle(), hToDraw.GetXaxis().GetTitle(), hToDraw.GetYaxis().GetTitle()))
    if hRatio != None: hRatio.SetTitle("MC/Data;;MC/Data")

    ## Set styles
    leg.SetNColumns(3)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)

    if hRD != None:
        hRD.SetMarkerSize(1.)
        hRD.SetMarkerColor(kBlack)
        hRD.SetLineColor(kBlack)
        hRD.SetMarkerStyle(kFullCircle)
    if hToDraw != None:
        hToDraw.GetXaxis().SetTitleSize(0.05)
        hToDraw.GetXaxis().SetTitleOffset(1.20)
        hToDraw.GetXaxis().SetLabelSize(0.04)
        hToDraw.GetYaxis().SetTitleSize(0.05)
        hToDraw.GetYaxis().SetTitleOffset(1.20)
        hToDraw.GetYaxis().SetLabelSize(0.04)

    if hRatio != None:
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

    if hToDraw != None:
        hToDraw.Draw("hist")
        hsMC.Draw("histsame")
        if hRD != None: hRD.Draw("sameLP")
        if hsNoStack != None: hsNoStack.Draw("same,nostack")
        hToDraw.Draw("axissame")
    leg.Draw()

    pad2 = c.cd(2)
    pad2.SetPad(0, 0, 1, 2./7)
    pad2.SetBottomMargin(0.12)

    if hRatio != None: hRatio.Draw("ep")

    c.Print("plots/%s/%s/%s.png" % (mode, stepName, hName))
    return c, pad1, pad2, leg, hRD, hMC, hsMC, hsNoStack
    

info = {}
info.update(yaml.load(open("config/plots.yaml")))
info.update(yaml.load(open("config/grouping.yaml")))
info.update(yaml.load(open("config/histogramming.yaml")))

imgs = {}
files = []
objs = {}
htmlElements = {}
for fName in glob("hist/*.root"):
    f = TFile(fName)
    mode = os.path.basename(fName)[:-5]

    for step in info['steps']:
        stepName = step['name']
        if stepName not in htmlElements: htmlElements[stepName] = []
        if not os.path.exists("plots/%s/%s" % (mode, stepName)): os.makedirs("plots/%s/%s" % (mode, stepName))
        for hName in step['hists']:
            d = f.Get("%s/h%s" % (stepName, hName))
            hRDs, hMCs, hNoStacks = [], [], []
            titles = [x.GetName() for x in d.GetListOfKeys()]
            for title in titles:
                h = d.Get(title)
                if h == None: continue
                h.AddBinContent(h.GetNbinsX(), h.GetBinContent(h.GetNbinsX()+1))

                ## Apply style
                color = None
                for histStyle in info['histStyles']:
                    if 'title' in histStyle and histStyle['title'] != title: continue
                    if 'color' in histStyle: color = histStyle['color']
                h.SetLineColor(kBlack)
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
                   not (canvasStyle['substr'] == '' or canvasStyle['substr'] in mode+'/'+stepName): continue
                if 'logy' in canvasStyle: opt['doLogY'] = canvasStyle['logy']

            obj = buildCanvas("%s/%s/%s" % (mode, stepName, hName), (hRDs, hMCs, hNoStacks), opt)
            #objs["%s/%s/%s" % (mode, stepName, hName)] = [c]#, hsMC, hMC, hRD, hRatio, leg]

            #obj[0].Print("plots/%s/%s/%s.png" % (mode, stepName, hName))
            htmlElements[stepName].append( "%s/%s/%s" % (mode, stepName, hName) )

    files.append(f)

with open("index.html", "w") as fout:
    print>>fout, """<html><head><title>plots</title></head><body>"""
    for stepName in sorted(htmlElements.keys()):
        print>>fout, """<h2>%s</h2>""" % stepName
        items = {}
        for x in htmlElements[stepName]:
            mode, step, name = x.split('/')
            if name not in items: items[name] = []
            items[name].append(x)
        for name in sorted(items.keys()):
            for item in sorted(items[name]):
                print>>fout, '<div style="display:inline-block;border:1px solid grey;"><span>{0}</span><br/><a href="plots/{0}.png"><img style="width:300px" src="plots/{0}.png"/></a></div>'.format(item)
            print>>fout, '<br/>'
    print>>fout, """</body></html>"""
