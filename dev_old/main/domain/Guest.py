from main.domain.GroceryCart import GroceryCart
from main.domain.Item import Item
from main.domain.TradingSystemException import AnomalyException
from main.domain.User import User
from main.security.Security import Security


class Guest(User):
	def __init__(self):
		super().__init__()
		self._groceryCarts = {}

	def login(self, username, password):
		return Security.verify(username, password)

	def register(self, username, password) -> bool:
		if Security.contains(username):
			return False
		return Security.add_user_password(username=username, password=password)

	def add_item_to_cart(self, item: Item, store_name: str) -> bool:
		if store_name not in self._groceryCarts.keys():
			self._groceryCarts[store_name] = GroceryCart(store_name)
		self._groceryCarts[store_name].add_item(item)
		return True

	def remove_item_from_cart(self, item: Item, store_name: str) -> bool:
		if store_name not in self._groceryCarts.keys():
			raise AnomalyException("store {} doesn't exist in your cart".format(store_name))
		self._groceryCarts[store_name].remove_item(item)
		return True

	def change_item_quantity_in_cart(self, item: Item, store_name: str, quantity: int) -> bool:
		if store_name not in self._groceryCarts.keys():
			raise AnomalyException("store {} doesn't exist in your cart".format(store_name))
		self._groceryCarts[store_name].change_item_quantity_in_cart(item, quantity)
		return True

	def watch_gc(self):
		return self._groceryCarts

	def check_quantity(self, item, store_name):
		return self._groceryCarts[store_name].items[item]

	def has_item_in_cart(self, item_name, store_name):
		if store_name not in self._groceryCarts.keys():
			return False
		return self._groceryCarts[store_name].has_item(item_name)
