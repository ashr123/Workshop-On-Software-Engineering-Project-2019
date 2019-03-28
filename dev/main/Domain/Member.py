from typing import List

from .Store import Store
from main.Domain.Permission import Permissions
from .Guset import Guest
from main.Domain import TradingSystem
from .User import User
from main.Domain import ManagementState
from .TradingSystemException import *


class Member(User):
	def __init__(self, name: str, guest: Guest):
		self._name: str = name
		self._stores_managed_states: List[ManagementState] = []
		self._guest: Guest = guest

	@property
	def name(self):
		return self._name

	@property
	def stores_managed_states(self):
		return self._stores_managed_states

	@property
	def get_guest(self):
		return self._guest

	def logout(self):
		return False

	def save_item_in_gc(self, item):  # TODO
		return False

	def watch_gc(self):  # TODO
		return False

	def add_managment_state(self, is_owner: bool, permissions_list: List[Permissions],
	                        store: Store) -> None:
		self._stores_managed_states.append(
			ManagementState(is_owner=is_owner, permissions_list=permissions_list, store=store))

	def add_manager(self, store: Store, member_name: str, permission_list: List[ManagementState.Permissions]):
		store_ind = list(filter(lambda s_m: s_m.store_name == store.get_name, self._stores_managed_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores : {} !".format(len(store_ind)))
		if len(store_ind) == 0:
			raise PermissionException("{} doesn't have permissions to add manager to {}".format(self.name, store.get_name))
		state: ManagementState = store_ind[0]
		if not state.is_owner:
			raise PermissionException("member name {} is not owner of the store:  !".format(self._name))
		new_manager: Member = TradingSystem.get_member(member_name=member_name)
		if new_manager is None:
			raise PermissionException("member_name {} is not a member at all !".format(member_name))
		new_manager.stores_managed_states.append(
			ManagementState(is_owner=False, permissions_list=permission_list, store=store))
		return True
