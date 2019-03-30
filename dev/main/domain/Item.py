from functools import reduce


class Item(object):
	def __init__(self, id: int, name: str, description: str, category: str, price: float, quantity: int):
		self._id = id
		self._name = name
		self._price = price
		self._description = description
		self._category = category
		self._quantity = quantity

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

	@property
	def category(self) -> int:
		return self._category

	def __str__(self):
		return "{}, {}, {}".format(self.name,self._description, self.price )

	def is_hashtaged(self, hashtag: str) -> bool:
		potential_tag_sources = [self._name, self._description, self._description]
		return reduce(lambda acc,curr:acc or hashtag in curr,potential_tag_sources,False)

