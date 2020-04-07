'''
File name:    model.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Model class, an abstract class implemented with Alert, Item, and Model classes.
              The class methods here are used within each class for database operations.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from typing import List,Dict, TypeVar, Type, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

# Establish type variable (T) to be used in Model
T = TypeVar('T',bound='Model')

# Classes derived from ABCMeta cannot be instantiated unless all of its abstract methods and properties are overridden.
class Model(metaclass=ABCMeta):

    collection:str     # Alert, Item, and Model each have a unique collection in the database
    _id:str            # All objects of Alert, Item, and Model are given a unique identifier

    # Model Constructor unnecessary because Model not used without implementation elsewhere
    def __init__(self):
        pass

    # Method saves objects to Mongo DB
    def save_to_mongo(self):
        Database.update(self.collection,{"_id": self._id},self.json())

    # Method removes objects from Mongo DB
    def remove_from_mongo(self):
        Database.remove(self.collection,{"_id": self._id})

    # Method produces a dictionary object to be used as json for Mongo DB operations
    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    # Method returns all items from class T (variable) as a Python list object
    @classmethod
    def all(cls:Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    # Method finds one object of class T with json search criteria
    @classmethod
    def find_one_by(cls:Type[T],attribute:str,value:Union[str,Dict]) -> T:
        return cls(**Database.find_one(cls.collection,{attribute:value}))

    # Method final all objects meeting a single search criteria
    @classmethod
    def find_many_by(cls:Type[T],attribute:str,value:Union[str,Dict]) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

    # Method finds object with attribute equal to its unique identifier
    @classmethod
    def get_by_id(cls:Type[T],_id: str) -> T:  #Item.get_by_id() -> Item, Alert.get_by_id() -> Alert
        return cls.find_one_by("_id",_id)
