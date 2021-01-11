#!/usr/bin/python3

import os

from typing import List

from pandas.core.frame import DataFrame #class

from portfolioDescription.portfolio1MethDescription import Portfolio1MethDescription #class

from input.inputRecomMLDefinition import InputRecomMLDefinition #class

from portfolioDescription.aPortfolioDescription import APortfolioDescription #class

from evaluationTool.evalToolSingleMethod import EToolSingleMethod #class

from recommenderDescription.recommenderDescription import RecommenderDescription #class

from input.inputSimulatorDefinition import InputSimulatorDefinition #class

from simulator.simulator import Simulator #class

from history.historyHierDF import HistoryHierDF #class

import pandas as pd
from input.aBatch import ABatch #class
from input.aBatch import BatchParameters #class

from input.aBatchST import ABatchST #class


class BatchSTSingle(ABatchST):

    @staticmethod
    def getParameters():

        aDict:dict = {}
        aDict[InputRecomMLDefinition.THE_MOST_POPULAR] = InputRecomMLDefinition.THE_MOST_POPULAR
        aDict[InputRecomMLDefinition.KNN] = InputRecomMLDefinition.KNN

        return aDict


    def run(self, batchID:str, jobID:str):

        divisionDatasetPercentualSize:int
        uBehaviour:str
        repetition:int
        divisionDatasetPercentualSize, uBehaviour, repetition = BatchParameters.getBatchParameters(self.datasetID)[batchID]

        recommenderID:str = self.getParameters()[jobID]

        rDescr:RecommenderDescription = InputRecomMLDefinition.exportInputRecomDefinition(recommenderID)

        pDescr:APortfolioDescription = Portfolio1MethDescription(recommenderID.title(), recommenderID, rDescr)

        simulator:Simulator = InputSimulatorDefinition.exportSimulatorSlantour(
                batchID, divisionDatasetPercentualSize, uBehaviour, repetition)
        simulator.simulate([pDescr], [DataFrame()], [EToolSingleMethod({})], HistoryHierDF)



if __name__ == "__main__":
   os.chdir("..")
   os.chdir("..")
   #print(os.getcwd())

   BatchSTSingle.generateBatches()