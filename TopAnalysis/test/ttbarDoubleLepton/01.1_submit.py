#!/usr/bin/env python
import os
modes = ["ElEl", "MuEl", "MuMu"]
nFilePerJob = int(os.environ["NFILE"]) if "NFILE" in os.environ else 5
if not os.path.exists("submit"): os.mkdir("submit")

import yaml
from glob import glob
procInfo = yaml.load(open("config/grouping.yaml").read())["processes"]
datasetInfo = {}
for f in glob("NanoAOD/2016/*.yaml"):
    for datasetGroup, dataset in yaml.load(open(f).read())['dataset'].iteritems():
        datasetInfo[datasetGroup] = dataset.keys()

fLists = []
for proc in procInfo:
    for datasetGroup in procInfo[proc]['datasets']:
        if datasetGroup not in datasetInfo: continue

        for dataset in datasetInfo[datasetGroup]:
            fLists.extend(glob("NanoAOD/2016/*/%s/%s.txt" % (datasetGroup, dataset.replace('/','.')[1:])))
fLists = list(set(fLists))

from math import ceil
for mode in modes:
    for fList in fLists:
        nFiles = len([x for x in open(fList).readlines() if len(x) != 0 and x[0] != '#'])
        nJobs = ceil(1.*nFiles/nFilePerJob)

        jobName = "%s.%s" % (mode, os.path.basename(fList)[:-4])
        cmd = "cd submit; create-batch bash ../01_prod_ntuple.sh %s ../%s %d --jobName %s -T --nJobs %d" % (mode, fList, nFilePerJob, jobName, nJobs)
        os.system(cmd)

