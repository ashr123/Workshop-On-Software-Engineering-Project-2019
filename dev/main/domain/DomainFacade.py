from typing import List

from .TradingSystem import TradingSystem
from .Member import Member
from .TradingSystemException import *
from main.domain import Store


class DomainFacade(object):
	@staticmethod
	def initiate_session():
		return TradingSystem.generate_id()

	@staticmethod
	def login(session_id, username, password):
		try:
			TradingSystem.login(session_id, username, password)
			return True
		except PermissionException as e:
			return False

	@staticmethod
	def logout(session_id):
		try:
			TradingSystem.logout(session_id)
			return True
		except PermissionException as e:
			return False

	@staticmethod
	def register(session_id, username, password):
		try:
			TradingSystem.register_member(session_id, username, password)
			return True
		except RegistrationExeption as e:
			return False

	@staticmethod
	def search_item(name=None, category=None, hashtag=None, range_filter=None, item_rank_filter=None, category_filter=None, store_rank_filter=None):
		return False

	@staticmethod
	def save_item(id):
		return False

	@staticmethod
	def watch_cart(session_id):
		user = TradingSystem.get_user(session_id)
		return user.watch_gc()

	@staticmethod
	def removeItemFromCart(id):
		return False

	@staticmethod
	def changeItemQuantityInCart(id):
		return False

	@staticmethod
	def buySingleItem(id):
		return False

	@staticmethod
	def buy_item_from_cart(ids):
		return False

	@staticmethod
	def pay(payment_details, address):
		return False

	@staticmethod
	def add_store(session_id: int, name: str, desc: str) -> bool:
		try:
			member: Member = TradingSystem.get_user_if_member(session_id)
			if member is None:
				raise GuestCannotOpenStoreException("User {} has no permission to open a store".format(name))
			if member.open_store(session_id=session_id,store_name=name, desc=desc):
				return True
		except UserAlreadyHasStoreException as e:
			return False
		except GuestCannotOpenStoreException as e:
			return False

	@staticmethod
	def add_item_to_store(session_id: int, store_name: str, itemName: str, desc: str, price: float, amount: int) -> bool:
		return False

	@staticmethod
	def remove_item_from_store(id: int, store_name: str):
		return False

	@staticmethod
	def change_item_in_store(id: int, store_name: str, field: str, value: float):
		return False

	@staticmethod
	def add_owner(owner_id: int, store_name: str):
		return False

	@staticmethod
	def remove_owner(owner_id: int, store_name: str):
		return False

	@staticmethod
	def add_manager(owner_id: int, store_name: str, permissions: List[str]):
		return False

	@staticmethod
	def remove_manager(owner_id: int, store_name: str):
		return False

	@staticmethod
	def remove_user(id: int):
		return False

	@staticmethod
	def setup(master_user, password):
		return False

	@staticmethod
	def add_item_to_cart(session_id: int, item_name: str, store_id: str):
		pass

	@staticmethod
	def open_store(owner_session: int, param):
		pass

	@staticmethod
	def get_member(session_id: int) -> Member:
		return TradingSystem.get_user(session_id)

	@staticmethod
	def get_store(session_id: int, store_name: str) -> Store:
		member = TradingSystem.get_user_if_member(session_id)
		if member == None:
			return None
		store_indicator = list(filter(lambda ms: ms.store.name == store_name, member.stores_managed_states))
		if len(store_indicator) == 0:
			return None
		return store_indicator[0].store
