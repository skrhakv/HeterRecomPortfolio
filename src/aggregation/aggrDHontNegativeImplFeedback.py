#!/usr/bin/python3
import random

import numpy as np
import pandas as pd

from numpy.random import beta
from typing import List

from pandas.core.frame import DataFrame #class
from pandas.core.series import Series #class

from aggregation.aAggregation import AAgregation #class
from aggregation.aggrDHont import AggrDHont #class

from aggregation.tools.negativeImplicitFeedback import NegativeImplicitFeedback #class

from history.aHistory import AHistory #class
from abc import ABC, abstractmethod

from userBehaviourDescription.userBehaviourDescription import UserBehaviourDescription #class


class AggrDHontNegativeImplFeedback(AggrDHont):

    ARG_SELECTORFNC:str = "selectorFnc"

    def __init__(self, uBehaviourDesc:UserBehaviourDescription, history:AHistory, argumentsDict:dict):
        if not isinstance(history, AHistory):
            raise ValueError("Argument history isn't type AHistory.")
        if type(argumentsDict) is not dict:
            raise ValueError("Argument argumentsDict isn't type dict.")

        self._uBehaviourDesc:UserBehaviourDescription = uBehaviourDesc
        self._history = history
        self._selectorFnc = argumentsDict[self.ARG_SELECTORFNC][0]
        self._selectorArg = argumentsDict[self.ARG_SELECTORFNC][1]
        self.argumentsDict:dict = argumentsDict.copy()
        self.argumentsDict.pop(self.ARG_SELECTORFNC)

    # methodsResultDict:{String:pd.Series(rating:float[], itemID:int[])},
    # modelDF:pd.DataFrame[numberOfVotes:int], numberOfItems:int
    def run(self, methodsResultDict:dict, modelDF:DataFrame, numberOfItems:int=20):

        # testing types of parameters
        if type(methodsResultDict) is not dict:
            raise ValueError("Type of methodsResultDict isn't dict.")
        if type(modelDF) is not DataFrame:
            raise ValueError("Type of methodsParamsDF isn't DataFrame.")
        if list(modelDF.columns) != ['votes']:
            raise ValueError("Argument methodsParamsDF doen't contain rights columns.")
        if type(numberOfItems) is not int:
            raise ValueError("Type of numberOfItems isn't int.")

        if sorted([mI for mI in modelDF.index]) != sorted([mI for mI in methodsResultDict.keys()]):
            raise ValueError("Arguments methodsResultDict and methodsParamsDF have to define the same methods.")
        for mI in methodsResultDict.keys():
            if modelDF.loc[mI] is None:
              raise ValueError("Argument modelDF contains in ome method an empty list of items.")
        if numberOfItems < 0:
            raise ValueError("Argument numberOfItems must be positive value.")

        methodsResultNewDict:List[int,np.Series[int,str]] =\
            NegativeImplicitFeedback.transformResultsOfMethods(methodsResultDict, self._uBehaviourDesc, self._history, numberOfItems=numberOfItems, argumentsDict=self.argumentsDict)

        itemsWithResposibilityOfRecommenders:List[int,np.Series[int,str]] =\
            super().run(methodsResultNewDict, modelDF, numberOfItems=numberOfItems)

        # list<(itemID:int, Series<(rating:int, methodID:str)>)>
        return itemsWithResposibilityOfRecommenders


    # methodsResultDict:{String:Series(rating:float[], itemID:int[])},
    # modelDF:DataFrame<(methodID:str, votes:int)>, numberOfItems:int
    def runWithResponsibility(self, methodsResultDict:dict, modelDF:DataFrame, numberOfItems:int=20):

        # testing types of parameters
        if type(methodsResultDict) is not dict:
            raise ValueError("Type of methodsResultDict isn't dict.")
        for methI in methodsResultDict.values():
            if type(methI) is not pd.Series:
                raise ValueError("Type of methodsParamsDF doen't contain Series.")
        if type(modelDF) is not DataFrame:
            raise ValueError("Type of methodsParamsDF isn't DataFrame.")
        if list(modelDF.columns) != ['votes']:
            raise ValueError("Argument methodsParamsDF doen't contain rights columns.")
        if type(numberOfItems) is not int:
            raise ValueError("Type of numberOfItems isn't int.")

        if sorted([mI for mI in modelDF.index]) != sorted([mI for mI in methodsResultDict.keys()]):
            raise ValueError("Arguments methodsResultDict and methodsParamsDF have to define the same methods.")
        for mI in methodsResultDict.keys():
            if modelDF.loc[mI] is None:
                raise ValueError("Argument modelDF contains in ome method an empty list of items.")
        if numberOfItems < 0:
            raise ValueError("Argument numberOfItems must be positive value.")


        methodsResultNewDict:List[int,np.Series[int,str]] =\
            NegativeImplicitFeedback.transformResultsOfMethods(methodsResultDict, self._uBehaviourDesc, self._history, numberOfItems=numberOfItems, argumentsDict=self.argumentsDict)

        itemsWithResposibilityOfRecommenders:List[int,np.Series[int,str]] =\
            super().runWithResponsibility(methodsResultNewDict, modelDF, numberOfItems=numberOfItems)

        # list<(itemID:int, Series<(rating:int, methodID:str)>)>
        return itemsWithResposibilityOfRecommenders
