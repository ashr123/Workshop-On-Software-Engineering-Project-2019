from main.Domain.User import User
from main.Domain.ManagementState import ManagementState
from main.Domain.TradingSystemException import *


class Member(User):

	def __init__(self, name):
		User.__init__(self)
		self._name = name
		self._storesManaged_states = []

	@property
	def name(self):
		return self._name

	@property
	def storesManaged_states(self):
		return self._storesManaged_states

	def logout(self):
		return False

	def openStore(self, name):
		state = ManagementState(isOwner=True)

	def add_manager(self, store_name, member_name, permission_list):
		storeInd = filter(lambda s_m: s_m.store_name == store_name, self._storesManaged_states)
		if len(storeInd) > 1:
			raise AnomalyException("Unexepted number of stores : {} !".format(len(storeInd)))
		if len(storeInd) == 0:
			raise PermissionException("{} doesn't have permissions to add manager to {}".format(self.name, store_name))
		state = storeInd[0]
		if not state.isOwner:
			raise PermissionException("member name {} is not owner of the store:  !".format(self._name))
		new_manager = self._tradingSystem.get_member(member_name)
		if new_manager == None:
			raise PermissionException("member_name {} is not a member at all !".format(member_name))
		new_manager.storesManaged_states.append(ManagementState(False, permission_list, store_name))
		return True
