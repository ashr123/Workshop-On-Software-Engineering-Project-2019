from functools import reduce
from .TradingSystemException import NoEnoughItemsException


class Item(object):
    def __init__(self, id: int, name: str, description: str, category: str, price: float, quantity: int):
        self._id = id
        self._name = name
        self._price = price
        self._description = description
        self._category = category
        self._quantity = quantity

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def quantity(self) -> str:
        return self._quantity

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, new_price: int):
        self._price = new_price

    @property
    def category(self) -> int:
        return self._category

    @property
    def desc(self) -> int:
        return self._description

    def inc_quantity(self, amount: int):
        self._quantity += amount

    def dec_quantity(self, amount: int):
        if amount > self._quantity:
            raise NoEnoughItemsException(
                message="Cannot decrease the amount of {} in {}, there are only {}".format(self.name, amount,
                                                                                           self._quantity))
        self._quantity -= amount

    def __str__(self):
        return "{}, {}, {}".format(self.name, self._description, self.price)

    def is_hashtaged(self, hashtag: str) -> bool:
        potential_tag_sources = [self._name.lower(), self._description.lower(), self._category.lower()]
        return reduce(lambda acc, curr: acc or hashtag.lower() in curr, potential_tag_sources, False)

    def edit_price(self, value):
        self._price = value

    def edit_name(self, value):
        self._name = value

    def edit_des(self, value):
        self._description = value

    def edit_category(self, value):
        self._category = value

    def edit_quantity(self, value):
        self._quantity = value