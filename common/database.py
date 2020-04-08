'''
File name:    database.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Database class which provides connection to a MongoDB database and methods
              for inserting, finding, and deleting database objects.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import pymongo
import os
from typing import Dict

class Database:

    URI = "mongodb://127.0.0.1:27017"
    CLIENT = pymongo.MongoClient(URI)
    DATABASE = CLIENT['BBC']

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query,data,upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        Database.DATABASE[collection].remove(query)