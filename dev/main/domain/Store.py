import copy
from typing import List

from .Item import Item
from .Rule import Rule
from main.domain import Member


class Store(object):
	def __init__(self, name: str, creator: Member, description: str):
		self._items: List[Item] = []
		self._name: str = name
		self._creator: Member = creator
		self._rules: List[Rule] = []
		# self._owners: List[Member] = []
		self._managers: List[Member] = [creator]
		self._desc: str = description

	@property
	def name(self) -> str:
		return self._name

	def add_item(self, new_item: Item):
		self._items.append(new_item)

	def remove_item(self, item_id: int) -> bool:  # TODO fix
		# if not item_name in map(lambda m: m.id, self._items):
		# 	raise PermissionException(message="this item id {} is not in store stock !".format(item_name))
		for item in self._items:
			if item.id == item_id:
				self._items.remove(item)
				return True
		return False

	def edit_item(self, item_id: int, new_price: float = None, new_name: str = None):  # TODO implement
		item = self.get_item(item_id)
		if item == None:
			return False
		if not new_name == None:
			item.name = new_name
		if not new_price == None:
			item.price = new_price
		self.remove_item(item_id=item_id)
		self.add_item(new_item=item)
		return True

	def add_owner(self, owner: Member):
		self._managers.append(owner)

	def has_item(self, item_id: int) -> bool:
		return item_id in list(map(lambda i: i.id, self._items))

	def get_item(self, item_id: int) -> Item:
		if not self.has_item(item_id):
			return None
		item = list(filter(lambda i: i.id == item_id, self._items))[0]
		return copy.deepcopy(item)

	def get_item_by_name(self, item_name) -> Item:
		item_list = list(filter(lambda i: i.name == item_name, self._items))
		if len(item_list) != 1:
			return None
		return item_list[0]
