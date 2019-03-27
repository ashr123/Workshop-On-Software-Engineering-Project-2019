from enum import Enum, auto
from typing import List


class ManagementState(object):
	class Permissions(Enum):
		PRE1 = auto()
		PRE2 = auto()

	def __init__(self, isOwner, permissions: List[Permissions], store_name: str):
		self._isOwner = isOwner
		self._permissions = permissions
		self._store_name = store_name

	@property
	def is_owner(self) -> bool:
		return self._isOwner

	@property
	def permissions(self) -> Permissions:
		return self._permissions

	@property
	def store_name(self):
		return self._store_name

	def add_item(self):
		return False

	def remove_item(self, item_id):
		return False

	def edit_item(self, item_id):
		return False

	def add_owner(self, member_id):
		return False

	def remove_owner(self, member_id):
		return False

	def add_manager(self, manager_Id):
		return False

	def remove_manager(self, manager_id):
		return False

	def set_manager_permissions(self, manager_id):
		return False
