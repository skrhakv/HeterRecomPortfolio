#!/usr/bin/python3
import random

import numpy as np
import pandas as pd

from numpy.random import beta
from typing import List
from typing import Dict #class

from pandas.core.frame import DataFrame #class
from pandas.core.series import Series #class

from aggregation.aAggregation import AAgregation #class
from aggregation.tools.responsibilityDHont import countDHontResponsibility #function
from aggregation.operators.rouletteWheelSelector import RouletteWheelSelector #class

from history.aHistory import AHistory #class
from abc import ABC, abstractmethod

from userBehaviourDescription.userBehaviourDescription import UserBehaviourDescription #class


class AggrFuzzyDHondt(AAgregation):

    ARG_SELECTOR:str = "selector"

    def __init__(self, history:AHistory, argumentsDict:dict):
        if not isinstance(history, AHistory):
            raise ValueError("Argument history isn't type AHistory.")
        if type(argumentsDict) is not dict:
            raise ValueError("Argument argumentsDict isn't type dict.")

        self._history = history
        self._selector = argumentsDict[self.ARG_SELECTOR]


    def update(self, ratingsUpdateDF:DataFrame, argumentsDict:Dict[str,object]):
        pass


    # methodsResultDict:{String:pd.Series(rating:float[], itemID:int[])},
    # modelDF:pd.DataFrame[numberOfVotes:int], numberOfItems:int
    def run(self, methodsResultDict:dict, modelDF:DataFrame, userID:int, numberOfItems:int, argumentsDict:Dict[str,object]={}):

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
      if type(argumentsDict) is not dict:
        raise ValueError("Argument argumentsDict isn't type dict.")

      candidatesOfMethods:np.asarray[str] = np.asarray([cI.keys() for cI in methodsResultDict.values()])
      uniqueCandidatesI:List[int] = list(set(np.concatenate(candidatesOfMethods)))
      #print("UniqueCandidatesI: ", uniqueCandidatesI)

      # numbers of elected candidates of parties
      electedOfPartyDictI:dict[str,int] = {mI:1 for mI in modelDF.index}
      #print("ElectedForPartyI: ", electedOfPartyDictI)

      # votes number of parties
      votesOfPartiesDictI:dict[str,float] = {mI:modelDF.votes.loc[mI] for mI in modelDF.index}
      #print("VotesOfPartiesDictI: ", votesOfPartiesDictI)

      recommendedItemIDs:List[int] = []

      iIndex:int
      for iIndex in range(0, numberOfItems):
        #print("iIndex: ", iIndex)

        if len(uniqueCandidatesI) == 0:
            return recommendedItemIDs[:numberOfItems]

        # coumputing of votes of remaining candidates
        actVotesOfCandidatesDictI:dict[int,int] = {}
        candidateIDJ:int
        for candidateIDJ in uniqueCandidatesI:
           votesOfCandidateJ:int = 0
           parityIDK:str
           for parityIDK in modelDF.index:
              partyAffiliationOfCandidateKJ:float = methodsResultDict[parityIDK].get(candidateIDJ, 0)
              votesOfPartyK:int = votesOfPartiesDictI.get(parityIDK)
              votesOfCandidateJ += partyAffiliationOfCandidateKJ * votesOfPartyK
           actVotesOfCandidatesDictI[candidateIDJ] = votesOfCandidateJ
        #print(actVotesOfCandidatesDictI)

        # select candidate with highest number of votes
        #selectedCandidateI:int = AggrDHont.selectorOfTheMostVotedItem(actVotesOfCandidatesDictI)
        selectedCandidateI:int = self._selector.select(actVotesOfCandidatesDictI)
        #print("SelectedCandidateI: " + str(selectedCandidateI))

        # add new selected candidate in results
        recommendedItemIDs.append(selectedCandidateI);

        # removing elected candidate from list of candidates
        uniqueCandidatesI.remove(selectedCandidateI)

        # updating number of elected candidates of parties
        electedOfPartyDictI:dict = {partyIDI:electedOfPartyDictI[partyIDI] + methodsResultDict[partyIDI].get(selectedCandidateI, 0) for partyIDI in electedOfPartyDictI.keys()}
        #print("DevotionOfPartyDictI: ", devotionOfPartyDictI)

        # updating number of votes of parties
        votesOfPartiesDictI:dict = {partyI: modelDF.votes.loc[partyI] / electedOfPartyDictI.get(partyI) for partyI in modelDF.index}
        #print("VotesOfPartiesDictI: ", votesOfPartiesDictI)

      # list<int>
      return recommendedItemIDs[:numberOfItems]


    # methodsResultDict:{String:Series(rating:float[], itemID:int[])},
    # modelDF:DataFrame<(methodID:str, votes:int)>, numberOfItems:int
    def runWithResponsibility(self, methodsResultDict:dict, modelDF:DataFrame, userID:int, numberOfItems:int, argumentsDict:Dict[str,object]={}):

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
        if type(argumentsDict) is not dict:
            raise ValueError("Argument argumentsDict isn't type dict.")

        aggregatedItemIDs:List[int] = self.run(methodsResultDict, modelDF, userID, numberOfItems)

        itemsWithResposibilityOfRecommenders:List[int,np.Series[int,str]] = countDHontResponsibility(
            aggregatedItemIDs, methodsResultDict, modelDF, numberOfItems)

        # list<(itemID:int, Series<(rating:int, methodID:str)>)>
        return itemsWithResposibilityOfRecommenders

