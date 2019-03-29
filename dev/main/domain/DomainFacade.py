from typing import List, Optional

from main.domain.Permission import Permissions
from .TradingSystem import TradingSystem
from .Member import Member
from .TradingSystemException import *
from main.domain import Store


class DomainFacade(object):
	@staticmethod
	def clear():
		TradingSystem.clear()

	@staticmethod
	def initiate_session():
		return TradingSystem.generate_id()

	@staticmethod
	def login(session_id: int, username: str, password: str):
		try:
			TradingSystem.login(session_id, username, password)
			return True
		except PermissionException as e:
			return e.msg

	@staticmethod
	def logout(session_id: int):
		try:
			TradingSystem.logout(session_id)
			return True
		except PermissionException as e:
			return False

	@staticmethod
	def register(session_id: int, username: str, password: str):
		try:
			TradingSystem.register_member(session_id, username, password)
			return True
		except RegistrationExeption as e:
			return e.msg

	@staticmethod
	def search_item(name: str = None, category=None, hashtag=None, fil_price=None, fil_rankStore=None,
	                fil_category=None, fil_rankItem=None):
		return False

	@staticmethod
	def save_item(item_name: str):
		return False

	@staticmethod
	def watch_cart(session_id: int):
		user = TradingSystem.get_user(session_id)
		return user.watch_gc()

	@staticmethod
	def remove_item_from_cart(item_name: str):
		return False

	@staticmethod
	def change_item_quantity_in_cart(item_name: str):
		return False

	@staticmethod
	def buy_single_item(item_name: str):
		return False

	@staticmethod
	def buy_item_from_cart(item_names: List[str]):
		return False

	@staticmethod
	def pay(payment_details, address: str):
		return False

	@staticmethod
	def add_store(session_id: int, name: str, desc: str) -> bool:
		try:
			member: Member = TradingSystem.get_user_if_member(session_id)
			if member is None:
				raise GuestCannotOpenStoreException("User {} has no permission to open a store".format(name))
			if member.open_store(session_id=session_id, store_name=name, desc=desc):
				return True
		except UserAlreadyHasStoreException as e:
			return False
		except GuestCannotOpenStoreException as e:
			return False

	@staticmethod
	def add_item_to_store(session_id: int, store_name: str, itemName: str, category: str, desc: str, price: float,
	                      amount: int) -> bool:
		return False

	@staticmethod
	def remove_item_from_store(item_name: str, store_name: str):
		return False

	@staticmethod
	def change_item_in_store(item_name: str, store_name: str, value: float):
		return False

	@staticmethod
	def add_owner(session_id: int, ownered_name: str, store_name: str):
		member: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
		if member is None:
			return "guest can't nominate owners"
		try:
			member.add_owner(store_name=store_name, member_name=ownered_name)
		except TradingSystemException as e:
			return e.msg
		return "OK"


	@staticmethod
	def remove_owner(session_id: int, owner_name: str, store_name: str):
		member: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
		if member is None:
			return "guest can't remove owners"
		try:
			member.remove_owner(store_name=store_name, member_name=owner_name)
		except TradingSystemException as e:
			return e.msg
		return "OK"

	@staticmethod
	def add_manager(owner_id: int, manager_name: str, store_name: str, permissions: List[str]):
		member: Optional[Member] = TradingSystem.get_user_if_member(session_id=owner_id)
		if member is None:
			return "guest can't nominate managers"
		try:
			member.add_manager(store_name=store_name, member_name=manager_name,
			                   permission_list=list(map(lambda permission: Permissions[permission], permissions)))
		except TradingSystemException as e:
			return e.msg
		return "OK"

	@staticmethod
	def remove_manager(owner_id: int, store_name: str):
		return False

	@staticmethod
	def remove_user(session_id: int, user_to_remove: str):
		return False

	@staticmethod
	def setup(master_user, password):
		try:
			TradingSystem.register_master_member(master_user, password)
			TradingSystem.connect_to_money_collection_system()
			TradingSystem.connect_to_product_supply_system()
			TradingSystem.connect_to_consistency_system()
		except TradingSystemException as e:
			return e.msg
		return True

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
		if member is None:
			return None
		store_indicator = list(filter(lambda ms: ms.store.name == store_name, member.stores_managed_states))
		if len(store_indicator) == 0:
			return None
		return store_indicator[0].store
