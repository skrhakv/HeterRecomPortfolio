#!/usr/bin/python3

import os

from typing import List

from pandas.core.frame import DataFrame #class

from portfolioDescription.portfolio1AggrDescription import Portfolio1AggrDescription #class

from evaluationTool.aEvalTool import AEvalTool #class
from evaluationTool.evalToolDHont import EvalToolDHont #class

from input.inputAggrDefinition import InputAggrDefinition, ModelDefinition  # class

from input.InputRecomDefinition import InputRecomDefinition #class

from input.batchesML1m.aML1MConfig import AML1MConf #function

from datasets.behaviours import Behaviours #class

from aggregation.toolsDHontNF.penalizationOfResultsByNegImpFeedback.aPenalization import APenalization #class

from aggregationDescription.aggregationDescription import AggregationDescription #class



class BatchNegDHontFixed:

    @staticmethod
    def getNegativeImplFeedbackParameters():

        pToolOLin0802HLin1002:APenalization = InputAggrDefinition.exportAPenaltyToolOLin0802HLin1002(AML1MConf.numberOfAggrItems)

        pToolOStat08HLin1002:APenalization = InputAggrDefinition.exportAPenaltyToolOStat08HLin1002(AML1MConf.numberOfAggrItems)

        aDict:dict = {}
        aDict["OLin0802HLin1002"] = pToolOLin0802HLin1002
        aDict["OStat08HLin1002"] = pToolOStat08HLin1002
        return aDict

    @staticmethod
    def getParameters():
        negativeImplFeedback:List[str] = BatchNegDHontFixed.getNegativeImplFeedbackParameters().keys()
        lrClicks:List[float] = [0.2, 0.1, 0.02, 0.005]
        lrViews:List[float] = [0.1 / 500, 0.1 / 200, 0.1 / 1000]

        aDict:dict = {}
        for nImplFeedbackI in negativeImplFeedback:
            for lrClickJ in lrClicks:
                for lrViewK in lrViews:
                    keyIJ:str = "Clk" + str(lrClickJ).replace(".", "") + "View" + str(lrViewK).replace(".", "") + nImplFeedbackI
                    eTool:AEvalTool = EvalToolDHont({EvalToolDHont.ARG_LEARNING_RATE_CLICKS: lrClickJ,
                                                 EvalToolDHont.ARG_LEARNING_RATE_VIEWS: lrViewK})
                    nImplFeedback:APenalization = BatchNegDHontFixed.getNegativeImplFeedbackParameters()[nImplFeedbackI]
                    aDict[keyIJ] = (nImplFeedback, eTool)
        return aDict


    def run(batchID:str, divisionDatasetPercentualSize:int, uBehaviour:str, repetition:int, jobID:str):

        #eTool:AEvalTool
        nImplFeedback, eTool = BatchNegDHontFixed.getParameters()[jobID]

        aConf:AML1MConf = AML1MConf(batchID, divisionDatasetPercentualSize, uBehaviour, repetition)

        rIDs, rDescs = InputRecomDefinition.exportPairOfRecomIdsAndRecomDescrs(aConf.datasetID)

        aDescNegDHontFixed:AggregationDescription = InputAggrDefinition.exportADescNegDHontFixed(nImplFeedback)

        pDescr:Portfolio1AggrDescription = Portfolio1AggrDescription(
            "NegDHontFixed" + jobID, rIDs, rDescs, aDescNegDHontFixed)

        model:DataFrame = ModelDefinition.createDHontModel(pDescr.getRecommendersIDs())

        aConf.run(pDescr, model, eTool)


    @staticmethod
    def generateBatches():

        divisionsDatasetPercentualSize:List[int] = [90]
        uBehaviours:List[str] = [Behaviours.COL_LINEAR0109, Behaviours.COL_STATIC08,
                                 Behaviours.COL_STATIC06, Behaviours.COL_STATIC04,
                                 Behaviours.COL_STATIC02]
        repetitions:List[int] = [1, 2, 3, 5]

        jobIDs:List[str] = list(BatchNegDHontFixed.getParameters().keys())

        for divisionDatasetPercentualSizeI in divisionsDatasetPercentualSize:
            for uBehaviourJ in uBehaviours:
                for repetitionK in repetitions:
                    for jobIDL in jobIDs:

                        batchID:str = "ml1mDiv" + str(divisionDatasetPercentualSizeI) + "U" + uBehaviourJ + "R" + str(repetitionK)
                        batchesDir:str = ".." + os.sep + "batches" + os.sep + batchID
                        if not os.path.exists(batchesDir):
                            os.mkdir(batchesDir)

                        job:str = str(BatchNegDHontFixed.__name__) + jobIDL
                        text:str = str(BatchNegDHontFixed.__name__) + ".run('"\
                                   + str(batchID) + "', "\
                                   + str(divisionDatasetPercentualSizeI) + ", '"\
                                   + str(uBehaviourJ) + "', "\
                                   + str(repetitionK) + ", "\
                                   + "'" + str(jobIDL) + "'" + ")"

                        jobFile:str = batchesDir + os.sep + job + ".txt"
                        BatchNegDHontFixed.__writeToFile(jobFile, text)


    @staticmethod
    def __writeToFile(fileName:str, text:str):
        f = open(fileName, "w")
        f.write(text)
        f.close()


if __name__ == "__main__":
   os.chdir("..")
   os.chdir("..")
   print(os.getcwd())
   BatchNegDHontFixed.generateBatches()