import uuid
from dataclasses import dataclass, field
from typing import Dict

from common.database import Database
from model.item import Item
from model.model import Model
from model.user.user import User

from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False,default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self):
        self.item.price = self.item.load_price()
        return self.item.price

    def notifiy_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.name} has reached a price under {self.price_limit}.  Latest price: {self.item.price}")
            Mailgun.send_mail(
                [self.user_email],
                 f'Notification for {self.name}',
                 '',
                 f'<p>Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}.</p><p>Go to this address to check your item: {self.item.url}</p>'
            )

    @classmethod
    def all(cls):
        elements_from_db = Database.find(cls.collection, {})
        alert_objects = []
        for elem in elements_from_db:
            alert = Alert(elem["name"],elem["item_id"],float(elem["price_limit"]),elem["user_email"], elem["_id"])
            alert_objects.append(alert)

        return alert_objects


    @classmethod
    def find_many_by_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(cls.collection, {"user_email": user_email})]