class Item(object):
	def __init__(self, id: int, name: str, price: int):
		self._id = id
		self._name = name
		self._price = price

	@property
	def id(self) -> int:
		return self._id

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def name(self, new_name):
		self._name = new_name

	@property
	def price(self) -> int:
		return self._price

	@price.setter
	def price(self, new_price: int):
		self._price = new_price