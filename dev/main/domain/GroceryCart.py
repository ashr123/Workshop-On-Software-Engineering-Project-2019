from main.domain.Item import Item


class GroceryCart(object):
	def __init__(self, s_name):
		self._items = {}
		self._store_name = s_name

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

	def remove_item(self, item_id):
		self._items.remove(item_id)

	def edit_item(self, item_id):
		return False

	def has_item(self, item_id):
		return item_id in list(map(lambda i: i.name, self._items))
