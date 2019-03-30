from typing import List, Optional

from main.domain import Store, TradingSystem
from main.domain.Permission import Permissions
from .Guest import Guest
from .User import User
from main.domain import ManagementState
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

	def logout(self):  # TODO implement
		return False

	def save_item_in_gc(self, item):  # TODO implement
		return False

	def watch_gc(self):  # TODO implement
		return False

	def add_managment_state(self, is_owner: bool, permissions_list: List[Permissions],
	                        store: Store, nominator) -> None:
		self._storesManaged_states.append(
			ManagementState.ManagementState(is_owner=is_owner, permissions_list=permissions_list, store=store, nominator=nominator))

	def add_manager(self, store_name: str, member_name: str, permission_list: List[ManagementState.Permissions]):
		store_ind = list(filter(lambda s_m: s_m.store.name == store_name, self._storesManaged_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores: {}!".format(len(store_ind)))
		if len(store_ind) == 0:
			raise PermissionException("{} doesn't have permissions to add manager to {}".format(self.name, store_name))
		state: ManagementState.ManagementState = store_ind[0]
		state.add_manager(manager_name=member_name, permissions_list=permission_list, nominator=self)

	def add_owner(self, store_name: str, member_name: str) -> None:
		store_ind = list(filter(lambda s_m: s_m.store.name == store_name, self._storesManaged_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores: {}!".format(len(store_ind)))
		if len(store_ind) == 0 or (not store_ind[0].is_owner):
			raise PermissionException("member name {} is not owner of the store!".format(self._name))
		state: ManagementState.ManagementState = store_ind[0]
		state.add_owner(member_name=member_name, nominator=self)

	def open_store(self, session_id: int, store_name: str, desc: str) -> bool:
		return TradingSystem.TradingSystem.open_store(session_id=session_id, store_name=store_name, desc=desc,
		                                              permissions_list=[])

	def get_store_management_state(self, store_name: str):
		management_states: List[ManagementState] = list(filter(lambda ms: ms.store.name == store_name, self.stores_managed_states))
		if len(management_states) == 0:
			return None
		return management_states[0]

	def remove_owner(self, store_name: str, member_name: str):
		store_ind = list(filter(lambda s_m: s_m.store.name == store_name, self._storesManaged_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores: {}!".format(len(store_ind)))
		if len(store_ind) == 0 or (not store_ind[0].is_owner):
			raise PermissionException("member name {} is not owner of the store!".format(self._name))
		state: ManagementState.ManagementState = store_ind[0]
		state.remove_manager(member_name, self, False)

	def remove_manager(self, store_name, member_name):
		store_ind = list(filter(lambda s_m: s_m.store.name == store_name, self._storesManaged_states))
		if len(store_ind) > 1:
			raise AnomalyException("Unexpected number of stores: {}!".format(len(store_ind)))
		if len(store_ind) == 0:
			raise PermissionException("member {} is not manager of the store!".format(self._name))
		state: ManagementState.ManagementState = store_ind[0]
		if state.is_owner or Permissions.REMOVE_MANAGER in state.permissions:
			state.remove_manager(manager_name=member_name, remover=self, is_master=False)
		else:
			raise PermissionException("member {} is not allowed to remove other managers!".format(self._name))

	def prepare_for_removal(self):
		for state in self._storesManaged_states:
			store: Store = state.store
			state.remove_manager(manager_name=self, remover=self, is_master=True)
			is_there_owner: bool = False
			for manager in store.managers:
				if manager.get_store_management_state(store.name).is_owner:
					is_there_owner = True
					break
			if not is_there_owner:
				TradingSystem.remove_store(store)
