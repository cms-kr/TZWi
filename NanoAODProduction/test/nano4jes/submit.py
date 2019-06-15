#!/usr/bin/env python
import os
baseDir = "NanoAOD/2016"
outBase = "/store/user/%s/nanoAOD/run2_2016v4_JESTuple_v1/20190614_1" % os.environ['USER']
jesType = "2016All"

if not os.path.exists("submit"): os.mkdir("submit")

from glob import glob
for fList in glob("%s/MC.RunIISummer16.central/*/*.txt" % baseDir)\
            +glob("%s/MC.RunIISummer16.rareprocess/*/*.txt" % baseDir):
    nFiles = len([x for x in open(fList).readlines() if len(x) != 0 and x[0] != '#'])
    jobName = "%s" % os.path.basename(fList)[:-4]
    cmd = "cd submit; create-batch bash ../run.sh %s ../%s --jobName %s -T --nJobs %d" % (jesType, fList, jobName, nFiles)
    cmd += " --transferDest %s/%s" % (outBase, jobName)
    os.system(cmd)
