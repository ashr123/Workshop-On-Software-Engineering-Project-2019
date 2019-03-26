from enum import Enum, auto


class ManagementState(object):
	class Premitions(Enum):
		PRE1 = auto()
		PRE2 = auto()

	def __init__(self, isOwner, permissions,store_name):
		self._isOwner = isOwner
		self._permissions = permissions
		self._store_name = store_name

	@property
	def isOwner(self):
		return self._isOwner

	@property
	def permissions(self):
		return self._permissions

	@property
	def store_name(self):
		return self._store_name

	def addItem(self):
		return False

	def removeItem(self, itemId):
		return False

	def editItem(self, itemId):
		return False

	def addOwner(self, memberId):
		return False

	def removeOwner(self, memberId):
		return False

	def addManager(self, managerId):
		return False

	def removeManager(self, managerId):
		return False

	def setManagerPermissions(self, managerId):
		return False
