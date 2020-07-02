#!/usr/bin/python3

from typing import List

from pandas.core.frame import DataFrame #class

from evaluationTool.evalToolSingleMethod import EToolSingleMethod #class

from input.inputsML1MDefinition import InputsML1MDefinition #class

from portfolioDescription.aPortfolioDescription import APortfolioDescription #class

from input.batchML1m.aConfig import ml1m #function

import pandas as pd



def jobSingleML1mTheMostPopular(batchID:str, divisionDatasetPercentualSize:int, uBehaviour:str, repetition:int):

        d = InputsML1MDefinition

        pDescs:List[APortfolioDescription] = [d.pDescTheMostPopular]
        models:List[DataFrame] = [pd.DataFrame()]
        evalTools:List = [EToolSingleMethod]

        ml1m(batchID, divisionDatasetPercentualSize, uBehaviour, repetition, pDescs, models, evalTools)