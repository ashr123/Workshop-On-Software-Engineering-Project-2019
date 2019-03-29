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
		self._managers: List[Member] = []
		self._desc: str = description

	@property
	def name(self) -> str:
		return self._name

	def add_item(self, new_item: Item):
		self._items.append(new_item)

	def remove_item(self, item_name: str) -> bool:  # TODO fix
		# if not item_name in map(lambda m: m.id, self._items):
		# 	raise PermissionException(message="this item id {} is not in store stock !".format(item_name))
		for item in self._items:
			if item.id == item_name:
				self._items.remove(item)
				return True
		return False

	def edit_item(self, itemId: str):
		return False

	def has_item(self, item: Item) -> bool:
		return item in self._items
