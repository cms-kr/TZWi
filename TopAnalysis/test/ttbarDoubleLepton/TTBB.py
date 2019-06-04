from HiggsAnalysis.CombinedLimit.PhysicsModel import *

### This base class implements signal yields by production and decay mode
### Specific models can be obtained redefining getHiggsSignalYieldScale
class TTBBModel(PhysicsModel):
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self, modelBuilder)
        self.modelBuilder.doModelBOnly = False
    def getYieldScale(self,bin,process):
        "Split in production and decay, and call getHiggsSignalYieldScale; return 1 for backgrounds "
        if not self.DC.isSignal[process]: return 1

        if process == "ttbb": return "TTBB"
        if process == "ttbj": return "TTBJ"
        if process == "ttcclf": return "TTCCLF"
        if process == "ttcclf2": return "k"   
        if process == "ttothers": return "k"   
    '''
    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("init="):
                if not self.freeTTBJ: 
                    initr = po.replace("init=","")
                    print initr
                else: 
                    initr = po.replace("init=","").split(",")[0]    
                    initrp = po.replace("init=","").split(",")[1]    
    '''
    def doParametersOfInterest(self):
        """create poi and other parameters, and define the poi set."""
        #initR = 0.01849
        #initK = 4.1
        #initk = 3.87

        
        #initR = 0.01344
        #initK = 4.9182
        initR = 0.01317
        initK = 2.411

        #self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 1.8, 3)) 
        self.modelBuilder.doVar("r[%f,%f,%f]"%(initR, 0.01, 0.025))
        #self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 1.8, 3)) 
        #self.modelBuilder.doVar("r[%f,%f,%f]"%(initR, 0.005, 0.02))
        self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 1.7, 3.1)) 
        #self.modelBuilder.doVar("r[%f,%f,%f]"%(initR, 0.005, 0.022))
        poi = "r"
        poi += ",k"
        self.modelBuilder.factory_("expr::TTBB(\"@0*@1\", k, r)")
        self.modelBuilder.factory_("expr::TTBJ(\"@0*@1\", k, r)")
        self.modelBuilder.factory_("expr::TTCCLF(\"-@0*@1\", k, r)")
        self.modelBuilder.doSet("POI",poi)

TTBBModel = TTBBModel()

