import copy
from typing import List, Optional

from .Item import Item
from .Rule import Rule
from .TradingSystemException import AnomalyException
from .TradingSystemException import ItemNotAvailableInStoreException


class Store(object):
    def __init__(self, name: str, creator, description: str, rules):
        self._items: List[Item] = []
        self._resereved_items = []
        self._name: str = name
        self._creator = creator
        self._rules: List[Rule] = []
        # self._owners= []
        self._managers = [creator]
        self._desc: str = description
        self._rank: int = 5
        self._rules = rules

    @property
    def name(self) -> str:
        return self._name

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def managers(self):
        return self._managers

    @property
    def rank(self):
        return self._rank

    def add_item(self, new_item: Item):
        self._items.append(new_item)

    def remove_item(self, item_id: int) -> bool:
        for item in self._items:
            if item.id == item_id:
                self._items.remove(item)
                return True
        return False

    def edit_item(self, item: Item, field: str, value: float):
        if field == "name":
            if self.get_item_by_name(value) is not None:
                raise AnomalyException("there's already an item named {} in the store {}".format(value, self.name))
            item.edit_name(value)
        elif field == "price":
            try:
                new_price = float(value)
            except ValueError:
                raise AnomalyException("price must be a float")
            if value < 0:
                raise AnomalyException("price must be a positive number")
            item.edit_price(new_price)
        elif field == "description":
            item.edit_des(value)
        elif field == "category":
            item.edit_category(value)
        elif field == "quantity":
            if isinstance(value, float):
                raise AnomalyException("quantity must be an int")
            if value < 0:
                raise AnomalyException("quantity must be a positive number")
            item.edit_quantity(value)
        else:
            raise AnomalyException("there is no such thing as {} in item".format(field))

    def add_owner(self, owner):
        self._managers.append(owner)

    def has_item(self, item_id: int) -> bool:
        return item_id in list(map(lambda i: i.id, self._items))

    def get_item(self, item_id: int) -> Optional[Item]:
        if not self.has_item(item_id):
            return None
        item = list(filter(lambda i: i.id == item_id, self._items))[0]
        return copy.deepcopy(item)

    def get_item_by_name(self, item_name) -> Item:
        item_list = list(filter(lambda i: i.name == item_name, self._items))
        if len(item_list) != 1:
            return None
        return item_list[0]

    def get_reserved_item_by_name(self, item_name) -> Item:
        item_list = list(filter(lambda i: i.name == item_name, self._resereved_items))
        if len(item_list) != 1:
            return None
        return item_list[0]

    def remove_manager(self, manager):
        for member in self.managers:
            if manager.name == member.name:
                self.managers.remove(member)
                return
        raise AnomalyException("store: manager not found!!")

    def search_item(self, name: str = None, category: str = None, hashtag: str = None, fil_price: int = None,
                    fil_category: str = None, fil_rankItem: str = None):
        ans = []
        ans += list(filter(lambda i: name != None and name in i.name, self._items))
        ans += list(filter(lambda i: hashtag != None and i.is_hashtaged(hashtag), self._items))
        ans += list(filter(lambda i: fil_price != None and i.price <= fil_price, self._items))
        ans += list(filter(lambda i: fil_category != None and fil_category in i.category, self._items))
        ans += list(filter(lambda i: fil_rankItem != None and i.rank >= fil_rankItem, self._items))
        return set(ans)

    def reserve_item(self, session_id: int, item_name: str, amount: int):
        item = self.get_item_by_name(item_name=item_name)
        if item is None:
            raise ItemNotAvailableInStoreException("{} not exist in {}".format(item_name, self.name))
        self.get_item_by_name(item_name=item_name).dec_quantity(amount)
        user_dict = list(filter(lambda dic: dic["session_id"] == session_id, self._resereved_items))
        if len(user_dict) == 0:
            self._resereved_items.append({"session_id": session_id, "reserved": []})
            user_dict = [self._resereved_items[-1]]
        item_res = list(filter(lambda dic: dic["item_id"] == item, user_dict[0]["reserved"]))
        if len(item_res) == 0:
            item_res = user_dict[0]["reserved"]
            item_res.append({"item_id": item.id, "amount": 0})
            item_res = list(item_res)
        item_res[0]["amount"] += amount

    # def add_reserved_item(self, item_name, amount):
    #     item = self.get_item_by_name(item_name=item_name)
    #     self._resereved_items.append({"session_id":session_id, "item_id": item, "amount": amount})

    def apply_trans(self, session_id, items):
        trans_items = self._resereved_items[session_id]
        for item in trans_items:
            if item in items:
                self._resereved_items[session_id][item] -= 1
