import uuid
from typing import Dict
from bs4 import BeautifulSoup
import re
import requests
from model.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default_factory=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __init__(self, url, tag_name, query, price=None, _id=None):
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def sample_item():
        URL = "https://www.bestbuy.com/site/acer-15-6-chromebook-intel-atom-x5-4gb-memory-16gb-emmc-flash-memory-granite-gray/6359610.p?skuId=6359610"
        TAG_NAME = "div"
        QUERY = {"class": "priceView-hero-price priceView-customer-price"}

        return Item(URL, TAG_NAME, QUERY)

    def load_price(self) -> float:
        HEADERS = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0", }
        response = requests.get(self.url, headers=HEADERS)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        print(self.tag_name)
        print(self.query)
        print(element)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+.\d+)")
        match = pattern.search(string_price)
        found_price = match.group(1)

        without_dollar_sign = found_price.replace("$", "")
        without_commas = without_dollar_sign.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def load_text(self) -> str:
        HEADERS = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0", }
        response = requests.get(self.url, headers=HEADERS)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()
        #
        # pattern = re.compile(r"(\$\d*,?\d*\.\d\d)")
        # match = pattern.search(string_price)
        # found_price = match.group(1)
        #
        # without_dollar_sign = found_price.replace("$","")
        # without_commas = without_dollar_sign.replace(",","")
        # self.price = float(without_commas)
        return string_price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
