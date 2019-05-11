#!/usr/bin/env python

import yaml
from glob import *
from ROOT import *
import os

odName = "hist"

info = {}
xsecSetFile = "config/crosssection.yaml"
histSetFile = "config/histogramming.yaml"
info.update(yaml.load(open(histSetFile)))
info.update(yaml.load(open(xsecSetFile)))
info.update(yaml.load(open("config/systematics.yaml")))
info.update(yaml.load(open("config/grouping.yaml")))
for f in glob("config/datasets/*.yaml"):
    if 'dataset' not in info: info['dataset'] = {}
    info['dataset'].update(yaml.load(open(f))['dataset'])

titleToProcs = {} ## for drawing
for proc, procInfo in info['processes'].iteritems():
    #for alias in aliases['datasets']: aliasToProc[alias] = proc
    title = procInfo['title']
    if title not in titleToProcs: titleToProcs[title] = []
    titleToProcs[title].append(proc)

fins = {}
scales = {}
for f in glob("raw_hist/*/*/*.root"):
    fin = TFile(f)
    fins[f.split('/',1)[-1]] = fin
    scale = 1.0
    hCutFlow = fin.Get("hCutFlow")
    nEvent = hCutFlow.GetBinContent(1)
    if nEvent != 0: scale /= nEvent
    scales[f.split('/',1)[-1]] = scale

## Plan how to merge histograms
def makedirs(d, dName):
    if '/' not in dName: return d.mkdir(dName)

    d1, d2 = dName.split('/',1)
    dNext = d.GetDirectory(d1)
    if dNext == None: dNext = d.mkdir(d1)
    return makedirs(dNext, d2)

if not os.path.exists(odName): os.makedirs(odName)
for mode in ["MuMu", "MuEl", "ElEl"]:
    fout = TFile("%s/%s.root" % (odName, mode), "recreate")
    hists = {}

    ## Loop over steps x histograms
    for stepInfo in info['steps']:
        for hName in stepInfo['hists']:
            if hName not in info['hists']: continue
            hinPath = "%s/h%s" % (stepInfo['name'], hName)

            ## open raw_hist root files
            for proc, procInfo in info['processes'].iteritems():
                datasets = procInfo['datasets']
                title = procInfo['title']
                longTitle = procInfo['longTitle'] if 'longTitle' in procInfo else title

                for alias in procInfo['datasets']:
                    if alias not in info['dataset']: continue
                    physProcName = alias.split('.',1)[-1]
                    xsec = info['crosssection'][physProcName] if physProcName in info['crosssection'] else 1.0

                    for ds in info['dataset'][alias].keys():
                        fName = "%s/%s/%s.root" % (mode, proc, ds[1:].replace('/', '.'))
                        if fName not in fins: continue
                        fin = fins[fName]
                        hin = fin.Get(hinPath)
                        if hin == None: continue

                        houtPath = "%s/%s" % (hinPath, title)
                        if houtPath not in hists:
                            hists[houtPath] = hin.Clone()
                            hists[houtPath].SetTitle(longTitle)
                            hists[houtPath].Reset()

                        hists[houtPath].Add(hin, xsec*scales[fName])

    for houtPath, h in sorted(hists.iteritems(), key=lambda x: x[0]):
        dout = fout.GetDirectory(os.path.dirname(houtPath))
        if dout == None: dout = makedirs(fout, os.path.dirname(houtPath))
        dout.cd()
        h.SetName(os.path.basename(houtPath))
        h.Write()

