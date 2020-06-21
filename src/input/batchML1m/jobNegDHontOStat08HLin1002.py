#!/usr/bin/python3

from typing import List

from pandas.core.frame import DataFrame #class

from evaluationTool.evalToolDHont import EvalToolDHont #class

from input.inputsML1MDefinition import InputsML1MDefinition #class

from portfolioDescription.aPortfolioDescription import APortfolioDescription #class

from input.batchML1m.aConfig import ml1m #function


def jobNegDHontOStat08HLin1002(divisionDatasetPercentualSize:int, repetition:int):

        d = InputsML1MDefinition

        pDescs:List[APortfolioDescription] = [d.pDescNegDHontOStat08HLin1002]
        models:List[DataFrame] = [d.modelNegDHontOStat08HLin1002DF]
        evalTools:List = [EvalToolDHont]

        ml1m("", divisionDatasetPercentualSize, repetition, pDescs, models, evalTools)