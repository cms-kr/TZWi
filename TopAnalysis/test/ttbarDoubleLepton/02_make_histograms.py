#!/usr/bin/env python
import yaml
import sys, os
from glob import glob
from multiprocessing import Pool, cpu_count

def runCmd(cmd):
    os.system(cmd)

if __name__ == '__main__':
    pool = Pool(processes=min(cpu_count, 20))

    ## Load all information
    info = {}
    histSetFile = "config/histogramming.yaml"
    info.update(yaml.load(open(histSetFile)))
    info.update(yaml.load(open("config/systematics.yaml")))
    info.update(yaml.load(open("config/grouping.yaml")))
    for f in glob("config/datasets/*.yaml"):
        if 'dataset' not in info: info['dataset'] = {}
        info['dataset'].update(yaml.load(open(f))['dataset'])

    aliasToProc = {}
    for proc, aliases in info['processes'].iteritems():
        for alias in aliases['datasets']: aliasToProc[alias.split('.',1)[-1]] = proc
    datasetToAlias = {}
    for alias, datasets in info['dataset'].iteritems():
        for dataset in datasets: datasetToAlias[dataset] = alias.split('.',1)[-1]

    ress = []
    for din in glob("ntuple/*/*/*"):
        channel, dataset = din.split('/')[2:]

        dataset = '/'+dataset.replace('.', '/')
        if dataset not in datasetToAlias: continue
        alias = datasetToAlias[dataset]
        if alias not in aliasToProc: continue
        proc = aliasToProc[alias]

        dout = "raw_hist/%s/%s" % (channel, proc)

        cut = info['processes'][proc]['cut'] if 'cut' in info['processes'][proc] else '1'
        weight = info['processes'][proc]['weight'] if 'weight' in info['processes'][proc] else '1'

        #os.system("NPROC=$(nproc) tzwi-makehistograms %s %s %s %s" % (cut, weight, histSetFile, d))
        res = pool.apply_async(os.system, ("tzwi-makehistograms '%s' '%s' %s %s %s" % (cut, weight, histSetFile, din, dout),))
        ress.append(res)

    for r in ress: r.get()
