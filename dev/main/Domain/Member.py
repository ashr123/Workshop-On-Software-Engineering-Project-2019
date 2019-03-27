from typing import List

from .Guset import Guest
from .TradingSystem import TradingSystem
from .User import User
from .ManagementState import ManagementState
from .TradingSystemException import *


class Member(User):
	def __init__(self, name: str, guest: Guest):
		self._name: str = name
		self._storesManaged_states: List[ManagementState] = []
		self._guest: Guest = guest

	@property
	def name(self):
		return self._name

	@property
	def stores_managed_states(self):
		return self._storesManaged_states

	@property
	def get_guest(self):
		return self._guest

	def logout(self):
		return False

	def save_item_in_gc(self, item):  # TODO
		return False

	def watch_gc(self):  # TODO
		return False

	def open_store(self, name: str, desc: str) -> bool:
		TradingSystem.open_store()

	def add_manager(self, store_name: str, member_name: str, permission_list: List[ManagementState.Permissions]):
		store_ind = list(filter(lambda s_m: s_m.store_name == store_name, self._storesManaged_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores : {} !".format(len(store_ind)))
		if len(store_ind) == 0:
			raise PermissionException("{} doesn't have permissions to add manager to {}".format(self.name, store_name))
		state = store_ind[0]
		if not state.is_owner:
			raise PermissionException("member name {} is not owner of the store:  !".format(self._name))
		new_manager = TradingSystem.get_member()
		if new_manager is None:
			raise PermissionException("member_name {} is not a member at all !".format(member_name))
		new_manager.stores_managed_states.append(
			ManagementState(isOwner=False, permissions=permission_list, store_name=store_name))
		return True
