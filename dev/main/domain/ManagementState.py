from typing import List

from main.domain.Permission import Permissions
from .Item import Item

from .TradingSystemException import PermissionException
from .Store import Store
from main.domain import TradingSystem, Member


class ManagementState(object):
	def __init__(self, is_owner: bool, permissions_list: List[Permissions], store: Store) -> None:
		self._isOwner: bool = is_owner
		self._permissions: List[Permissions] = permissions_list
		self._store: Store = store

	@property
	def is_owner(self) -> bool:
		return self._isOwner

	@property
	def permissions(self) -> List[Permissions]:
		return self._permissions

	@property
	def store(self) -> Store:
		return self._store

	def add_item(self, item_id: int, name: str, price: int) -> bool:  # 1
		if Permissions.ADD_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		if self.store.add_item(Item(item_id, name, price)):
			return True
		return False

	def remove_item(self, item_name: str) -> bool:  # 2
		if Permissions.REMOVE_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		if self.store.remove_item(item_name):
			return True
		return False

	def edit_item(self, item_name: str, new_price: float = None, new_name: str = None) -> bool:  # 3
		if Permissions.EDIT_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		self.store.edit_item(item_name=item_name, new_price=new_price, new_name=new_name)
		return False

	def add_owner(self, member_name: str) -> bool:  # 4
		if not self.is_owner:
			raise PermissionException(message="you don't have the permission to add owner, you ar not the creator!")
		owner: Member.Member = TradingSystem.TradingSystem.get_member(member_name=member_name)
		if len(list(filter(lambda state: state.store.name == self.store.name and state.is_owner, owner.stores_managed_states))) > 0:
			raise PermissionException(message="you're already an owner of this store!")
		owner.add_managment_state(is_owner=True, [])
		self.store.add_owner(owner=owner)
		return False

	def remove_owner(self, owner_name: str) -> bool:  # 5

		return False

	def add_manager(self, manager_name) -> bool:  # 6
		# if not self.permissions[6] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def remove_manager(self, manager_id) -> bool:  # 7
		# if not self.permissions[7] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def set_manager_permissions(self, manager_id) -> bool:  # 8
		# if not self.permissions[8] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False
