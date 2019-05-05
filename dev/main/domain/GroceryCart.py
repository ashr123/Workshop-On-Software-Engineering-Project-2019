from typing import Dict

from main.domain.Item import Item
from main.domain.TradingSystemException import AnomalyException


class GroceryCart(object):
    def __init__(self, s_name):
        self._items: Dict[Item, int] = {}
        self._store_name: str = s_name

    @property
    def store_name(self):
        return self._store_name

    @property
    def items(self):
        return self._items

    def add_item(self, item: Item):
        if item in self._items.keys():
            self._items[item] += 1
        else:
            self._items[item] = 1

    def remove_item(self, item: Item):
        try:
            self._items.pop(item)
        except KeyError:
            raise AnomalyException("item {} doesn't exist i your cart".format(item.id))

    def change_item_quantity_in_cart(self, item: Item, quantity: int):
        if item not in self._items.keys():
            raise AnomalyException("item {} doesn't exist in your cart".format(item.id))
        curr_quantity = self._items[item]
        if quantity < 0 and curr_quantity < abs(quantity):
            raise AnomalyException(
                "operation of decrease quantity failed, given: {}, existing: {}".format(quantity, curr_quantity))
        self._items[item] += quantity

    def has_item(self, item_id):
        return item_id in list(map(lambda i: i.name, self._items))
