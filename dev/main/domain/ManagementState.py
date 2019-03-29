from typing import List, Optional

from main.domain.Permission import Permissions
from .Item import Item

from .TradingSystemException import PermissionException, AnomalyException
from .Store import Store
from main.domain import TradingSystem


class ManagementState(object):
	def __init__(self, is_owner: bool, permissions_list: List[Permissions], store: Store, nominator):
		self._isOwner: bool = is_owner
		self._permissions: List[Permissions] = permissions_list
		self._nominator = nominator
		self._store: Store = store

	@property
	def is_owner(self) -> bool:
		return self._isOwner

	@is_owner.setter
	def is_owner(self, is_owner: bool):
		_isOwner = is_owner

	@property
	def permissions(self) -> List[Permissions]:
		return self._permissions

	@property
	def store(self) -> Store:
		return self._store

	@property
	def nominator(self):
		return self._nominator

	def add_item(self, item_id: int, name: str, price: int) -> bool:
		if not self.is_owner and Permissions.ADD_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		if self.store.add_item(Item(item_id, name, price)):
			return True
		return False

	def remove_item(self, item_name: str) -> bool:
		if not self.is_owner and Permissions.REMOVE_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		if self.store.remove_item(item_name):
			return True
		return False

	def edit_item(self, item_name: str, new_price: float = None, new_name: str = None) -> bool:
		if not self.is_owner and Permissions.EDIT_ITEM not in self._permissions:
			raise PermissionException(message="you don't have the permission to do this auction!")
		self.store.edit_item(item_name=item_name, new_price=new_price, new_name=new_name)
		return False

	def add_owner(self, member_name: str, nominator) -> None:
		if not self.is_owner:
			raise PermissionException(message="you don't have the permission to add owner!")
		new_owner = TradingSystem.TradingSystem.get_member(member_name=member_name)
		if new_owner is None:
			raise AnomalyException("member to be ownered doesn't exists")
		if len(list(filter(lambda state: state.store.name == self.store.name and state.is_owner,
		                   new_owner.stores_managed_states))) > 0:
			raise PermissionException(message="you're already an owner of this store! (circular nomination)")
		existing_management_state: Optional[ManagementState] = new_owner.get_store_management_state(self.store.name)
		if existing_management_state is not None:
			existing_management_state.is_owner = True
		else:
			new_owner.add_managment_state(is_owner=True, permissions_list=[], store=self._store, nominator=nominator)
			self.store.add_owner(owner=new_owner)


	def remove_owner(self, owner_name: str, remover) -> None:  # see: section 4.4
		owner = TradingSystem.TradingSystem.get_member(member_name=owner_name)
		existing_management_state: Optional[ManagementState] = owner.get_store_management_state(self.store.name)
		if remover.name != existing_management_state._nominator.name:
			raise PermissionException(message="owner can't remove another owner that he didn't nominate")
		else:
			self.store.remove_manager(manager=owner)
			for manager in self.store.managers:
				manager_state: ManagementState = manager.get_store_management_state(self.store.name)
				manager_nominator = manager_state.nominator
				if manager_nominator is not None and manager_nominator.name == owner_name:
					existing_management_state.remove_owner(manager.name, owner)
			owner.stores_managed_states.remove(existing_management_state)

	def add_manager(self, manager_name) -> bool:
		# if not self.permissions[6] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def remove_manager(self, manager_id) -> bool:
		# if not self.permissions[7] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False

	def set_manager_permissions(self, manager_id) -> bool:
		# if not self.permissions[8] == True:
		# 	raise PermissionException(message="you d'ont have the permission to do this auction !")
		return False
