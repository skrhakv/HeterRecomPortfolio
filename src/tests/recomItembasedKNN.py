#!/usr/bin/python3

import os

from configuration.configuration import Configuration #class

from pandas.core.frame import DataFrame #class
from pandas.core.series import Series #class

from datasets.ml.ratings import Ratings #class
from datasets.ml.items import Items #class

from recommender.aRecommender import ARecommender #class
from recommender.recommenderItemBasedKNN import RecommenderItemBasedKNN #class

from history.historyDF import HistoryDF #class

from datasets.aDataset import ADataset #class
from datasets.datasetML import DatasetML #class
from datasets.datasetRetailrocket import DatasetRetailRocket #class
from datasets.datasetST import DatasetST #class

import pandas as pd


def test01():
    print("Test 01")

    print("Running RecommenderItemBasedKNN ML:")

    ratingsDF:DataFrame = Ratings.readFromFileMl1m()

    filmsDF:DataFrame = Items.readFromFileMl1m()

    # Take only first 50k
    ratingsDFTrain:DataFrame = ratingsDF.iloc[0:50000]

    trainDataset:ADataset = DatasetML("test", ratingsDFTrain, pd.DataFrame(), filmsDF)

    # train recommender
    rec:ARecommender = RecommenderItemBasedKNN("test", {})
    rec.train(HistoryDF("test01"), trainDataset)

    # get one rating for update
    ratingsDFUpdate:DataFrame = ratingsDF.iloc[50005:50006]

    # get recommendations:
    print("Recommendations before update")
    r:Series = rec.recommend(ratingsDFUpdate['userId'].iloc[0], 50, {})

    rec.update(ARecommender.UPDT_CLICK, ratingsDFUpdate)

    print("Recommendations after update")
    r: Series = rec.recommend(ratingsDFUpdate['userId'].iloc[0], 50, {})

    print("Test for non-existent user:")
    r:Series =rec.recommend(10000, 50, {})
    print(r)
    print("================== END OF TEST 01 ======================\n\n\n\n\n")


def test02():
    print("Test 02")

    print("Running RecommenderItemBasedKNN ML:")

    ratingsDF:DataFrame = Ratings.readFromFileMl1m()

    filmsDF:DataFrame = Items.readFromFileMl1m()

    ratingsDFTrain:DataFrame = ratingsDF.iloc[0:1000000]

    trainDataset:ADataset = DatasetML("test", ratingsDFTrain, pd.DataFrame(), filmsDF)

    # train recommender
    rec:ARecommender = RecommenderItemBasedKNN("test", {})
    rec.train(HistoryDF("test02"), trainDataset)

    r:Series = rec.recommend(1, 50, {})
    print(r)
    print("================== END OF TEST 02 ======================\n\n\n\n\n")


def test03():
    print("Test 03")

#    userID: 23
#    currentItemID: 196
#    repetition: 0

    print("Running RecommenderItemBasedKNN ML:")

    ratingsDF:DataFrame = Ratings.readFromFileMl1m()
    ratingsSortedDF:DataFrame = ratingsDF.sort_values(by=Ratings.COL_TIMESTAMP)

    filmsDF:DataFrame = Items.readFromFileMl1m()

    print(len(ratingsSortedDF))
    ratingsDFTrain:DataFrame = ratingsSortedDF[0:900000]
    ratingsDFTrain: DataFrame = ratingsDFTrain[ratingsDFTrain[Ratings.COL_USERID] != 23]
    ratingsDFTrain: DataFrame = ratingsDFTrain[ratingsDFTrain[Ratings.COL_MOVIEID] != 10]


    print(ratingsDFTrain.head(25))

    trainDataset:ADataset = DatasetML("test", ratingsDFTrain, pd.DataFrame(), filmsDF)


    # train recommender
    rec:ARecommender = RecommenderItemBasedKNN("test1", {})
    rec.train(HistoryDF("test03"), trainDataset)


    uDdata = [[23, 10, 4, 10000]]
    uDF: DataFrame = pd.DataFrame(uDdata, columns=[Ratings.COL_USERID, Ratings.COL_MOVIEID, Ratings.COL_RATING, Ratings.COL_TIMESTAMP])

    rec.update(ARecommender.UPDT_CLICK, uDF)


    r:Series = rec.recommend(23, 10, {})
    print(r)
    print("\n")

    r:Series = rec.recommend(23, 10, {})
    print(r)

    print("================== END OF TEST 03 ======================\n\n\n\n\n")


def test04():
    print("Test 04")

    print("Running RecommenderItemBasedKNN RR:")

    from datasets.retailrocket.events import Events  # class
    eventsDF:DataFrame = Events.readFromFile()

    dataset:ADataset = DatasetRetailRocket("test", eventsDF, DataFrame(), DataFrame())

    rec:ARecommender = RecommenderItemBasedKNN("test", {})
    print("train")
    rec.train(HistoryDF("test"), dataset)

    uDF:DataFrame = DataFrame([eventsDF.iloc[9000]])
    print(uDF)
    rec.update(ARecommender.UPDT_CLICK, uDF)

    recommendation = rec.recommend(1, 20, {})
    print(recommendation)

    print("================== END OF TEST 04 ======================\n\n\n\n\n")


def test05():
    print("Test 05")

    print("Running RecommenderItemBasedKNN ST:")

    from datasets.slantour.events import Events  # class
    eventsDF:DataFrame = Events.readFromFile()

    dataset:ADataset = DatasetST("test", eventsDF, DataFrame())

    rec:ARecommender = RecommenderItemBasedKNN("test", {})
    rec.train(HistoryDF("test"), dataset)

    uDF:DataFrame = DataFrame([eventsDF.iloc[9000]])
    print(uDF)
    rec.update(ARecommender.UPDT_CLICK, uDF)

    r = rec.recommend(3325463, 20, {})
    print(r)

    print("================== END OF TEST 05 ======================\n\n\n\n\n")


if __name__ == "__main__":
    os.chdir("..")

    #test01()
    #test02()
    #test03()
    #test04()
    test05()