import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class btagWeightProducer(Module, object):
    def __init__(self, *args, **kwargs):
        #super(TTbarDoubleLepton, self).__init__(*args, **kwargs)
        self.jetIndexBrName = kwargs["jetIndex"] if "jetIndex" in kwargs else ""

        sfName = "Jet_btagSF_deepjet_shape" if "btagAlgo" not in kwargs else kwargs["btagAlgo"]
        self.sfNames = [sfName]
        for syst in ["jes", "lf", "hf", "hfstats1", "hfstats2", "lfstats1", "lfstats2", "cferr1", "cferr2"]:
            for d in ["up", "down"]:
                self.sfNames.append("%s_%s_%s" % (sfName, d, syst))

        self.in_Jet_index = None

        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("BtagWeight", "D")
        for sfName in self.sfNames[1:]:
            self.out.branch("BtagWeight_%s" % sfName[4:], "D")

        self.initReaders(inputTree, self.out._tree)
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def initReaders(self,tree,outTree):
        for sfName in self.sfNames:
            setattr(self, 'in_%s' % sfName, self.out._tree.GetBranch(sfName).GetLeaf(sfName))

        if self.jetIndexBrName != "":
            self.in_Jet_index = self.out._tree.GetBranch(self.jetIndexBrName).GetLeaf(self.jetIndexBrName)

        self._ttreereaderversion = tree._ttreereaderversion
        pass
    def analyze(self, event):
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree, self.out._tree)

        if self.jetIndexBrName != "":
            goodJetIdxs = event._tree.b_out_GoodJet_index
            goodJetIdxs = [goodJetIdxs.at(i) for i in range(goodJetIdxs.size())]
        else:
            goodJetIdxs = range(int(event._tree.valueReader("nJet")))

        branch = getattr(self, 'in_%s' % self.sfNames[0])
        weight = 1.0
        for i in goodJetIdxs: weight *= branch.GetValue(i)
        self.out.fillBranch("BtagWeight", weight)

        for sfName in self.sfNames[1:]:
            weight = 1.0
            branch = getattr(self, 'in_%s' % sfName)
            for i in goodJetIdxs: weight *= branch.GetValue(i)
            self.out.fillBranch("BtagWeight_%s" % sfName[4:], weight)

        return True

btagWeight = lambda: btagWeightProducer(jetIndex="GoodJet_index")
btagWeightWithAllJets = lambda: btagWeightProducer()
