import copy
from typing import List, Optional

from .Item import Item
from .Rule import Rule
from .TradingSystemException import AnomalyException


class Store(object):
	def __init__(self, name: str, creator, description: str):
		self._items: List[Item] = []
		self._name: str = name
		self._creator = creator
		self._rules: List[Rule] = []
		# self._owners= []
		self._managers = [creator]
		self._desc: str = description
		self._rank: int = 5

	@property
	def name(self) -> str:
		return self._name

	@property
	def items(self) -> str:
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

	def edit_item(self, item_id: int, new_price: float = None, new_name: str = None):
		item = self.get_item(item_id)
		if item == None:
			return False
		if not new_name is None:
			item.name = new_name
		if not new_price is None:
			item.price = new_price
		self.remove_item(item_id=item_id)
		self.add_item(new_item=item)
		return True

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
