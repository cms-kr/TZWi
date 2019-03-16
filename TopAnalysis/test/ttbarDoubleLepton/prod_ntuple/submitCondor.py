#!/usr/bin/env python
import sys, os

runScript = sys.argv[1]
fileLists = sys.argv[2:]

maxFiles = 100

jds = """# condor jds
universe   = vanilla
log = ntuple/condor.log
getenv     = True
should_transfer_files = YES
#requirements = "OpSysMajorVer == 6"

executable = %s
""" % runScript

for fileList in fileLists:
    pathName = os.path.basename(os.path.dirname(fileList))
    jobName = os.path.basename(fileList).replace(".txt", "").replace("dataset_", "")

    nFiles = len(open(fileList).readlines())
    if nFiles % maxFiles == 0: nJobs = nFiles/maxFiles
    else: nJobs = nFiles/maxFiles+1

    if not os.path.exists("job/%s/%s" % (pathName, jobName)):
        os.makedirs("job/%s/%s" % (pathName, jobName))
    if not os.path.exists("ntuple/%s/%s" % (pathName, jobName)):
        os.makedirs("ntuple/%s/%s" % (pathName, jobName))

    fout = open("job/%s/%s/condor.jds" % (pathName, jobName), "w")
    print>>fout, jds
    print>>fout, "arguments  = %s %d $(Process)" % (fileList, maxFiles)
    print>>fout, "output = job/%s/%s/job_$(Process).log" % (pathName, jobName)
    print>>fout, "error = job/%s/%s/job_$(Process).err" % (pathName, jobName)
    print>>fout, "queue %d" % nJobs
    print>>fout, ""
    fout.close()

    os.system("condor_submit job/%s/%s/condor.jds" % (pathName, jobName))
