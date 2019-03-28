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

	@property
	def price(self) -> int:
		return self._price
