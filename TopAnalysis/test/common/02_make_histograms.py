#!/usr/bin/env python
import yaml
import sys, os
import subprocess
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
    procInfo = yaml.load(open("config/grouping.yaml"))["processes"]
    #systConfig = yaml.load(open("config/systematics.yaml"))["systematics"] ## FIXME: To be implemented later

    ## Build CMS official dataset full name to process group mapping
    dsetfullname2procs = {}
    for proc in procInfo:
        for dataset in procInfo[proc]['datasets']:
            if dataset not in datasetConfig: continue
            for dsetfullname in datasetConfig[dataset]:
                if dsetfullname not in dsetfullname2procs: dsetfullname2procs[dsetfullname] = []
                dsetfullname2procs[dsetfullname].append(proc)

    if os.path.exists("raw_hist"):
      path = "raw_hist"
      subprocess.call(["rm", "-rf", path])
    ress = []
    for din in glob("ntuple/*/*/*"):
        mode, dataset = din.split('/')[2:]
        dataset = '/'+dataset.replace('.', '/')
        if dataset not in dsetfullname2procs: continue

        for proc in dsetfullname2procs[dataset]:
            config = procInfo[proc]
            if 'modes' in config and mode not in config['modes']: continue

            dout = "raw_hist/%s/%s" % (mode, proc)

            cut = config['cut'] if 'cut' in config else '1'
            weight = config['weight'] if 'weight' in config else '1'

            #os.system("NPROC=$(nproc) tzwi-makehistograms %s %s %s %s" % (cut, weight, histSetFile, d))
            res = pool.apply_async(os.system, ("tzwi-makehistograms '%s' '%s' %s %s %s" % (cut, weight, histSetFile, din, dout),))
            ress.append(res)

    for r in ress: r.get()
