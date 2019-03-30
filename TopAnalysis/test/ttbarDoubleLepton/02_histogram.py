#!/usr/bin/env python

from ROOT import *
import yaml
import sys, os
from array import array

dataType = sys.argv[1]
fName = sys.argv[2]

config = yaml.load(open("../../data/histogramming/ttbbDilepton.yaml"))
steps = config['steps']
hists = config['hists']
weight0 = config['common'+dataType]['weight']

chain = TChain("Friends")
for fName in sys.argv[2:]: chain.Add(fName)
gROOT.SetBatch(True)

if 'NPROOF' in os.environ:
    nProc = os.environ['NPROOF']
    prf = TProof.Open("", "workers=%s" % nProc)
    chain.SetProof(True)

ofName = fName.replace('ntuple', 'hist')
odName = os.path.dirname(ofName)
if not os.path.exists(odName): os.makedirs(odName)

oFile = TFile(ofName, 'recreate')
oFile.cd()
hCutFlow_noWeight = TH1D("hCutFlow_noWeight", "Cut Flow (noWeight);Step;Events (unweighted)", len(steps), 0, len(steps))
hCutFlow = TH1D("hCutFlow", "Cut Flow;Step;Events", len(steps), 0, len(steps))

for istep, step in enumerate(steps):

    hCutFlow_noWeight.GetXaxis().SetBinLabel(istep+1, step['name'])
    hCutFlow.GetXaxis().SetBinLabel(istep+1, step['name'])

    weight = weight0
    if 'weight' in step: weight = '(%s)*(%s)' % (weight0, step['weight'])

    cut = step['cut']
    oFile.cd()
    chain.Draw("%d>>+hCutFlow_noWeight" % (istep), "(%s)*(%s)" % (weight, cut), "goff")
    chain.Draw("%d>>+hCutFlow" % (istep), "(%s)*(%s)" % (weight, cut), "goff")

    if 'hists' not in step: continue

    dout = oFile.mkdir(step['name'])
    dout.cd()

    for hname, hdef in [(x, hists[x]) for x in step['hists'] if x in hists]:
        h = None
        bins = hdef['bins']
        if type(bins) == list:
            h = TH1D(hname, hdef['title'], len(bins)-1, array('d', bins))
        else:
            h = TH1D(hname, hdef['title'], bins['nbins'], bins['xmin'], bins['xmax'])
        h.SetDirectory(dout)

        expr = hdef['expr'] if 'expr' in hdef else hname
        chain.Draw("%s>>%s" % (expr, hname), "%s*(%s)" % (weight, cut), "goff")
        #chain.Draw("%s>>%s" % (expr, hname), "1*(%s)" % (weight), "goff")

        h.Write()

    oFile.cd()

hCutFlow_noWeight.Write()
hCutFlow.Write()
oFile.Close()
