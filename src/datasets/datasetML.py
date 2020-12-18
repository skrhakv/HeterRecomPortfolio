#!/usr/bin/python3

from pandas.core.frame import DataFrame #class

from datasets.aDataset import ADataset #class

from datasets.ml.items import Items #class
from datasets.ml.ratings import Ratings #class
from datasets.ml.users import Users #class

class DatasetML(ADataset):

    def __init__(self, ratingsDF:DataFrame, usersDF:DataFrame, itemsDF:DataFrame):
        if type(ratingsDF) is not DataFrame:
            raise ValueError("Argument ratingsDF isn't type DataFrame.")
        if type(usersDF) is not DataFrame:
            raise ValueError("Argument usersDF isn't type DataFrame.")
        if type(itemsDF) is not DataFrame:
            raise ValueError("Argument itemsDF isn't type DataFrame.")

        self.ratingsDF:DataFrame = ratingsDF
        self.usersDF:DataFrame = usersDF
        self.itemsDF:DataFrame = itemsDF

    @staticmethod
    def readDatasets():
        # dataset reading
        ratingsDF:DataFrame = Ratings.readFromFileMl1m()
        usersDF:DataFrame = Users.readFromFileMl1m()
        itemsDF:DataFrame = Items.readFromFileMl1m()

        return DatasetML(ratingsDF, usersDF, itemsDF)