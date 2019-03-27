from main.Domain.GroceryCart import GroceryCart
from main.Domain.User import User


class Guest(User):
	def __init__(self):
		super().__init__()
		self._groceryCarts = GroceryCart()

	@property
	def get_trading_system(self):
		return

	def login(self, username, password):
		return False

	def watch_gc(self):
		return str(self._groceryCarts)
