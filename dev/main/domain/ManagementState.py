from enum import Enum, auto
from typing import List

from main.domain.Permission import Permissions
from .Item import Item

from .TradingSystemException import PermissionException
from .Store import Store


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

	def add_item(self, _id: int, name: str, price: int) -> bool:  # 1
		if Permissions.ADD_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		new_item = Item(_id, name, price)
		if self.store.add_item(new_item):
			return True
		return False

	def remove_item(self, item_id: int) -> bool:  # 2
		if Permissions.REMOVE_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		if self.store.remove_item(item_id):
			return True
		return False

	def edit_item(self, itemId, new_id, new_name, new_price) -> bool:  # 3
		if Permissions.EDIT_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		# todo
		return False

	def add_owner(self, oarator_name: str, member_name: str) -> bool:  # 4
		# if not self.store._creator_name == oarator_name:
		# 	raise PermissionException(message="you d'ont have the permission to add owner ,you ar not the creator !")
		return False

	def remove_owner(self, oarator_name: str, memberId) -> bool:  # 5
		# if not self.store. == oarator_name:
		# 	raise PermissionException(message="you d'ont have the permission to remove owner ,you ar not the creator !")
		return False

	def add_manager(self, managerId) -> bool:  # 6
		# if not self.permissions[6] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def remove_manager(self, managerId) -> bool:  # 7
		# if not self.permissions[7] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def set_manager_permissions(self, managerId) -> bool:  # 8
		# if not self.permissions[8] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False
