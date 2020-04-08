'''
File name:    store.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Store class with attributes and methods including the methods used to retrieve
              the correct store based on an item url.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from typing import Dict
import uuid
import re
from model.model import Model
from dataclasses import dataclass, field
from common.database import Database

# Store class established as a dataclass which extends the Model class
@dataclass(eq=False)
class Store(Model):
    # No explicit constructor is needed for a dataclass - it is implied
    collection: str = field(init=False,default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # Store object translated into json object for interaction with Mongo DB
    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    # Method returns Store object given unique store id
    @classmethod
    def get_by_id(cls,_id: str) -> "Store":
        return cls.find_one_by("_id",_id)

    # Method returns Store object based on store name
    @classmethod
    def get_by_name(cls,store_name: str) -> "Store":
        return cls.find_one_by("name",store_name)

    # Method returns Store object matching search criteria specified as a json object
    @classmethod
    def find_one_by(cls,attribute:str,value:str) -> "Store":
        print(attribute)
        return cls(**Database.find_one(cls.collection,{attribute:value}))

    # Method returns Store object based on the url prefix
    @classmethod
    def get_by_url_prefix(cls,url_prefix) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix",url_regex)

    # Method returns Store object from Item url, finding the store with by matching regular expression
    @classmethod
    def find_by_url(cls,url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        print(url_prefix)
        store = cls.get_by_url_prefix(url_prefix)
        print(store._id)
        return store