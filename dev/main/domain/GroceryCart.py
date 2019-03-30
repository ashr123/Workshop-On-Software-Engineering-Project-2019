from main.domain.Item import Item


class GroceryCart(object):
	def __init__(self):
		self._items = {}

	def add_item(self, item: Item):
		# if self._items
		# self._items.append(item_id)
		pass

	def remove_item(self, item_id):
		self._items.remove(item_id)

	def edit_item(self, item_id):
		return False

	def has_item(self, item_id):
		return item_id in list(map(lambda i: i.name, self._items))
