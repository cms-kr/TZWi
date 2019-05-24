#!/usr/bin/env python
import os
modes = ["ElEl", "MuEl", "MuMu"]
nFilePerJob = int(os.environ["NFILE"]) if "NFILE" in os.environ else 5
if not os.path.exists("submit"): os.mkdir("submit")

import yaml
from glob import glob
config = yaml.load(open("config/grouping.yaml").read())
for f in glob("NanoAOD/2016/*.yaml"):
    config.update(yaml.load(open(f).read()))

fLists = []
for proc in config['processes']:
    datasetGroups = config['processes'][proc]['datasets']
    for datasetGroup in datasetGroups:
        if datasetGroup not in config['dataset']: continue

        datasets = config['dataset'][datasetGroup].keys()
        for dataset in datasets:
            fLists.extend(glob("NanoAOD/2016/*/%s/%s.txt" % (datasetGroup, dataset.replace('/','.')[1:])))

from math import ceil
for mode in modes:
    for fList in fLists:
        nFiles = len([x for x in open(fList).readlines() if len(x) != 0 and x[0] != '#'])
        nJobs = ceil(1.*nFiles/nFilePerJob)

        jobName = "%s.%s" % (mode, os.path.basename(fList)[:-4])
        cmd = "create-batch bash ../01_prod_ntuple.sh %s ../%s %d --jobName %s -T --nJobs %d" % (mode, fList, nFilePerJob, jobName, nJobs)
        os.system(cmd)

