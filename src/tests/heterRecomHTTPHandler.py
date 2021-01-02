#!/usr/bin/python3

import os
import _thread
import time
from httpServer.httpServer import HeterRecomHTTPHandler #class

from http.server import BaseHTTPRequestHandler, HTTPServer

from typing import Dict
from pandas import DataFrame

from history.aHistory import AHistory #class
from history.historyDF import HistoryDF #class

from datasets.aDataset import ADataset #class
from datasets.datasetST import DatasetST #class
from datasets.slantour.events import Events #class

from recommender.aRecommender import ARecommender #class
from recommender.recommenderTheMostPopular import RecommenderTheMostPopular #class
from recommender.recommenderCosineCB import RecommenderCosineCB #class
from recommender.recommenderW2V import RecommenderW2V #class
from recommender.recommenderItemBasedKNN import RecommenderItemBasedKNN #class
from recommender.recommenderBPRMF import RecommenderBPRMF #class

from portfolio.aPortfolio import APortfolio #class

from portfolioDescription.portfolio1MethDescription import Portfolio1MethDescription #class

from recommenderDescription.recommenderDescription import RecommenderDescription #class



def startS():
    print("Starting Http server")
    server = HTTPServer(('', 8080), HeterRecomHTTPHandler)
    server.serve_forever()


def test01():
    print("Test 01")

    rDescr: RecommenderDescription = RecommenderDescription(RecommenderTheMostPopular, {})

    recommenderID: str = "TheMostPopular"
    pDescr: Portfolio1MethDescription = Portfolio1MethDescription(recommenderID.title(), recommenderID, rDescr)

    dataset: ADataset = DatasetST.readDatasets()

    history: AHistory = HistoryDF("test")
    p: APortfolio = pDescr.exportPortfolio("jobID", history)
    p.train(history, dataset)

    portfolioDict: Dict[str, APortfolio] = {HeterRecomHTTPHandler.VARIANT_A: p}
    modelsDict: Dict[str, int] = {HeterRecomHTTPHandler.VARIANT_A: DataFrame()}

    HeterRecomHTTPHandler.portfolioDict = portfolioDict
    HeterRecomHTTPHandler.modelsDict = modelsDict


    # Run HTTP in separate thread
    try:
        _thread.start_new_thread(startS, ())
    except:
        print("Error: unable to start HTTP Server thread")

    time.sleep(3)

    itemID:int = 555
    userID:int = 1

    command1:str = "curl -sS 'http://127.0.0.1:8080/?" +\
                    HeterRecomHTTPHandler.ARG_ACTIONID + "=" + HeterRecomHTTPHandler.ACTION_UPDATE + "&" +\
                    HeterRecomHTTPHandler.ARG_VARIANTID + "=" + HeterRecomHTTPHandler.VARIANT_A + "&" + \
                    HeterRecomHTTPHandler.ARG_ITEMID + "=" + str(itemID) + "&" + \
                    HeterRecomHTTPHandler.ARG_USERID + "=" + str(userID) + "'"
    print(command1)
    os.system(command1)

    command2:str = "curl -sS 'http://127.0.0.1:8080/?" +\
                    HeterRecomHTTPHandler.ARG_ACTIONID + "=" + HeterRecomHTTPHandler.ACTION_RECOMMEND + "&" +\
                    HeterRecomHTTPHandler.ARG_VARIANTID + "=" + HeterRecomHTTPHandler.VARIANT_A + "&" + \
                    HeterRecomHTTPHandler.ARG_USERID + "=" + str(userID) + "&" +\
                    HeterRecomHTTPHandler.ARG_NUMBER_OF_ITEMS + "=20" + "'"
    print(command2)
    os.system(command2)


    time.sleep(3)


if __name__ == '__main__':
    os.chdir("..")

    test01()