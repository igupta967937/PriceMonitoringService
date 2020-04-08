'''
File name:    item.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Item class with attributes and methods including the methods used to get
              the current price of a product.  The Item class extends Model, implements abstract methods and
              inherits database methods.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import uuid
from typing import Dict
from bs4 import BeautifulSoup
import re
import requests
from model.model import Model
from dataclasses import dataclass, field

# Item class established as a dataclass which extends the Model class
@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default_factory=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # Constructor for Item objects fully specified
    def __init__(self, url, tag_name, query, price=None, _id=None):
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    # Method to produce sample Item object
    @staticmethod
    def sample_item():
        URL = "https://www.bestbuy.com/site/acer-15-6-chromebook-intel-atom-x5-4gb-memory-16gb-emmc-flash-memory-granite-gray/6359610.p?skuId=6359610"
        TAG_NAME = "div"
        QUERY = {"class": "priceView-hero-price priceView-customer-price"}

        return Item(URL, TAG_NAME, QUERY)

    # Method to load the current price of the Item object
    def load_price(self) -> float:
        # Header needed to avoid sites that prohibit web scrapers
        HEADERS = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0", }

        # Response object utilizes requests.get() method to retrieve all website information
        response = requests.get(self.url, headers=HEADERS)

        # The content attribute of the response object contains the website content
        content = response.content

        # BeutifulSoup object used for parsing the html document
        soup = BeautifulSoup(content, "html.parser")

        # Tag name and query used to retrieve the html element containing the item price
        element = soup.find(self.tag_name, self.query)

        # Price (as a string) obtained by stripping out white space
        string_price = element.text.strip()

        # Price extracted from string using a regular expression pattern matcher
        pattern = re.compile(r"(\d+.\d+)")
        match = pattern.search(string_price)
        found_price = match.group(1)

        # Removing $ and , from the string and casting as a float
        without_dollar_sign = found_price.replace("$", "")
        without_commas = without_dollar_sign.replace(",", "")
        self.price = float(without_commas)

        # Returning price - a float
        return self.price

    # Method converts Item object to json object for interaction with Mongo DB
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
