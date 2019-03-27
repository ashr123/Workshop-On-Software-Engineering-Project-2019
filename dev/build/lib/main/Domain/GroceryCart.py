class GroceryCart(object):
	def __init__(self, items):
		self._items = items

	def addItem(self, itemId):
		self._items.add(itemId)

	def removeItem(self, itemId):
		self._items.remove(itemId)

	def editItem(self, itemId):
		return False
