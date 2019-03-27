from .Item import Item
from .Rule import Rule
from .Member import Member
from .TradingSystemException import PermissionException

class Store(object):
	def __init__(self, name: str, creator_name: str,description :str):
		self._items: list = []
		self._name = name
		self._creator_name = creator_name
		self._rules: list = []
		self._owners: list = []
		self._managers: list = []
		self._desc= description

	def add_item(self, new_item: Item):
		self._items.append(new_item)

	def remove_item(self, item_id: int) ->  bool:
		# if not item_id in map(lambda m: m.id, self._items):
		# 	raise PermissionException(message="this item id {} is not in store stock !".format(item_id))
		for item in self._items :
			if item.id == item_id :
				self._items.remove(item)
				return  True
		return  False


	def edit_item(self, itemId: str):
		return False
