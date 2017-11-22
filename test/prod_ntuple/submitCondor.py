#!/usr/bin/env python
import sys, os

runScript = sys.argv[1]
fileLists = sys.argv[2:]

maxFiles = 25

fout = open("condor.jds", "w")
print>>fout, """# condor jds
universe   = vanilla
log = ntuple/condor.log
getenv     = True
should_transfer_files = YES

output = ntuple/log/job_$(Process).log
error = ntuple/log/job_$(Process).err
#requirements = "OpSysMajorVer == 6"

executable = %s
""" % runScript

if not os.path.exists("ntuple/log"): os.makedirs("ntuple/log")

for fileList in fileLists:
    print>>fout, "arguments  = %s %d $(Process)" % (fileList, maxFiles)
    nFiles = len(open(fileList).readlines())
    if nFiles % maxFiles == 0: nJobs = nFiles/maxFiles
    else: nJobs = nFiles/maxFiles+1
    print>>fout, "queue %d" % nJobs
    print>>fout, ""
fout.close()

os.system("condor_submit condor.jds")
