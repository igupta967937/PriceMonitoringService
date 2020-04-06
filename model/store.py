
from typing import Dict
import uuid
import re
from model.model import Model
from dataclasses import dataclass, field
from common.database import Database

@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False,default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls,_id: str) -> "Store":
        return cls.find_one_by("_id",_id)

    @classmethod
    def get_by_name(cls,store_name: str) -> "Store":
        return cls.find_one_by("name",store_name)

    @classmethod
    def find_one_by(cls,attribute:str,value:str) -> "Store":
        return cls(**Database.find_one(cls.collection,{attribute:value}))

    @classmethod
    def get_by_url_prefix(cls,url_prefix) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix",url_regex)

    @classmethod
    def find_by_url(cls,url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        print(url_prefix)
        store = cls.get_by_url_prefix(url_prefix)
        print(store._id)
        return store