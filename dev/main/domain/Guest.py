from main.domain.GroceryCart import GroceryCart
from main.domain.User import User
from main.security.Security import Security
from .TradingSystemException import UserAlreadyExistException
from .TradingSystemException import PermissionException
from main.domain import TradingSystem


class Guest(User):
	def __init__(self):
		super().__init__()
		self._groceryCarts = GroceryCart()

	def login(self, username, password):
		return Security.verify(username, password)

	def register(self, username, password) -> bool:
		if Security.contains(username):
			return False
		return Security.add_user_password(username=username, password=password)

	def watch_gc(self):
		return str(self._groceryCarts)
