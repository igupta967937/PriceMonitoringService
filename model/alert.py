'''
File name:    alert.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Alert class with attributes and methods including the methods used to get
              the current price of a product and to send alerts by email when appropriate.  The Alert class extends
              Model, implements abstract methods and inherits database methods.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import uuid
from dataclasses import dataclass, field
from typing import Dict
from common.database import Database
from model.item import Item
from model.model import Model
from model.user.user import User
from libs.mailgun import Mailgun

# Alert class established as a dataclass which extends the Model class
@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False,default="alerts")  # Mongo DB collection
    name: str                                             # Product name
    item_id: str                                          # Unique identifier for Items class
    price_limit: float                                    # The alert price at which customer wishes to be notified
    user_email: str                                       # User's email address
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)  # Unique identifier for the alert

    # Constructor adds Item object and User object to alert
    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    # Establishes unique json object for each alert object to be used with Mongo DB
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    # Method calls load_price() method from Item class
    def load_item_price(self):
        self.item.price = self.item.load_price()
        return self.item.price

    # Method compares the current price to the established user limit and sends email notification to the user
    # if the item price is now lower than the alert price limit.
    def notifiy_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.name} has reached a price under {self.price_limit}.  Latest price: {self.item.price}")
            Mailgun.send_mail(
                [self.user_email],
                 f'Notification for {self.name}',
                 '',
                 f'<p>Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}.</p><p>Go to this address to check your item: {self.item.url}</p>'
            )

    # Method retrieves all alerts from application database
    @classmethod
    def all(cls):
        elements_from_db = Database.find(cls.collection, {})
        alert_objects = []
        for elem in elements_from_db:
            alert = Alert(elem["name"],elem["item_id"],float(elem["price_limit"]),elem["user_email"], elem["_id"])
            alert_objects.append(alert)

        return alert_objects

    # Method returns a list of all alerts which have the specified email address
    @classmethod
    def find_many_by_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(cls.collection, {"user_email": user_email})]