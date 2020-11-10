#!/usr/bin/python3

import os

from typing import List

from pandas.core.frame import DataFrame #class

from portfolioDescription.portfolio1MethDescription import Portfolio1MethDescription #class

from input.InputRecomDefinition import InputRecomDefinition #class

from portfolioDescription.aPortfolioDescription import APortfolioDescription #class

from input.batchesML1m.aML1MConfig import AML1MConf #function

from evaluationTool.evalToolSingleMethod import EToolSingleMethod #class

from recommenderDescription.recommenderDescription import RecommenderDescription #class

import pandas as pd
from input.aBatch import ABatch #class


class BatchSingle(ABatch):

    def getParameters(self):

        aDict:dict = {}
        aDict[InputRecomDefinition.COS_CB_MEAN] = InputRecomDefinition.COS_CB_MEAN
        aDict[InputRecomDefinition.COS_CB_WINDOW3] = InputRecomDefinition.COS_CB_WINDOW3
        aDict[InputRecomDefinition.THE_MOST_POPULAR] = InputRecomDefinition.THE_MOST_POPULAR
        aDict[InputRecomDefinition.W2V_POSNEG_MEAN] = InputRecomDefinition.W2V_POSNEG_MEAN
        aDict[InputRecomDefinition.W2V_POSNEG_WINDOW3] = InputRecomDefinition.W2V_POSNEG_WINDOW3

        return aDict


    def run(self, batchID:str, jobID:str):

        from execute.generateBatches import BatchParameters #class
        divisionDatasetPercentualSize:int
        uBehaviour:str
        repetition:int
        divisionDatasetPercentualSize, uBehaviour, repetition = BatchParameters.getBatchParameters()[batchID]

        recommenderID:str = self.getParameters()[jobID]

        aConf:AML1MConf = AML1MConf(batchID, divisionDatasetPercentualSize, uBehaviour, repetition)

        rDescr:RecommenderDescription = InputRecomDefinition.exportInputRecomDefinition(recommenderID, aConf.datasetID)

        pDescr:APortfolioDescription = Portfolio1MethDescription(recommenderID.title(), recommenderID, rDescr)

        model:DataFrame = pd.DataFrame()
        eTool:List = EToolSingleMethod({})

        aConf.run(pDescr, model, eTool)



if __name__ == "__main__":
   os.chdir("..")
   os.chdir("..")
   print(os.getcwd())
   BatchSingle.generateBatches()