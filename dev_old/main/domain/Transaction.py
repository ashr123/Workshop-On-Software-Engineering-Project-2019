from functools import reduce


class Transaction(object):

	def __init__(self, id, session_id,store_name):
		self._id = id
		self._session_id = session_id
		self._store_name = store_name
		self._items = []

	@property
	def id(self):
		return self._id

	@property
	def store_name(self):
		return self._store_name

	@property
	def items(self):
		return self._items

	def add_item(self, item_name):
		return self._items.append(item_name)

