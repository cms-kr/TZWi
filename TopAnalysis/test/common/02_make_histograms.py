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
    histSetFile = "config/histogramming.yaml"
    datasetConfig = {}
    for f in glob("config/datasets/*.yaml"): datasetConfig.update(yaml.load(open(f))['dataset'])
    groupConfig = yaml.load(open("config/grouping.yaml"))["processes"]
    #systConfig = yaml.load(open("config/systematics.yaml"))["systematics"] ## FIXME: To be implemented later

    ## Build CMS official dataset full name to process group mapping
    dsetfullname2procs = {}
    for proc in groupConfig:
        for dataset in groupConfig[proc]['datasets']:
            if dataset not in datasetConfig: continue
            for dsetfullname in datasetConfig[dataset]:
                if dsetfullname not in dsetfullname2procs: dsetfullname2procs[dsetfullname] = []
                dsetfullname2procs[dsetfullname].append(proc)

    ress = []
    for din in glob("ntuple/*/*/*"):
        channel, dataset = din.split('/')[2:]
        dataset = '/'+dataset.replace('.', '/')
        if dataset not in dsetfullname2procs: continue

        for proc in dsetfullname2procs[dataset]:
            config = groupConfig[proc]
            if 'channels' in config and channel not in config['channels']: continue

            dout = "raw_hist/%s/%s" % (channel, proc)

            cut = config['cut'] if 'cut' in config else '1'
            weight = config['weight'] if 'weight' in config else '1'

            #os.system("NPROC=$(nproc) tzwi-makehistograms %s %s %s %s" % (cut, weight, histSetFile, d))
            res = pool.apply_async(os.system, ("tzwi-makehistograms '%s' '%s' %s %s %s" % (cut, weight, histSetFile, din, dout),))
            ress.append(res)

    for r in ress: r.get()
