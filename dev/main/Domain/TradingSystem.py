from .TradingSystemException import UserAlreadyExistException
from .TradingSystemException import PermissionException
from main.security.Security import Security
from .Guset import Guest
from .Member import Member
from .Store import Store
from .User import User
from typing import *


class TradingSystem(object):

	def __init__(self):
		self._users: Dict[int, User] = {}
		self._members: List[Member] = []
		self._stores: List[Store] = []

	def get_user(self, session_id: int) -> User:
		return self._users[session_id]

	def get_member(self, member_name: str) -> Optional[Member]:
		if member_name in map(lambda member: member.name, self._members):
			return list(filter(lambda member: member.name == member_name, self._members))[0]
		return None

	def generate_id(self) -> int:
		"""
		Generates new session ID
		:rtype: int
		:return: The new ID
		"""
		new_session_id: int = len(self._users)
		self._users[new_session_id] = Guest(tradingSystem=self)
		return new_session_id

	def search(self, keyword):
		return False

	def register_member(self, session_id: int, username: str, password: str) -> bool:
		if username in map(lambda m: m.name, self._members):
			raise UserAlreadyExistException(message="the user {} is already registered".format(username))
		if
		self._members[session_id] = Member(username)  # TODO - handle security

	def login(self, session_id: int, username: str, password: str) -> bool:
		if not username in map(lambda m: m.name, self._members):
			raise PermissionException(message="the user {} is not a member !".format(username))
		if not Security.verify(username, password):
			raise PermissionException(message="the user {} can not login !".format(username))
		try_to_log_in = self.get_user(session_id)
		if not isinstance(try_to_log_in,Guest):
			raise PermissionException(message="the user {} already login !".format(username))
		new_logged_in_member =Member(try_to_log_in)
		self._users[username] = new_logged_in_member
		return True

	def logout(self, session_id: int) -> bool:
		try_to_logout = self.get_user(session_id)
		if not isinstance(try_to_logout,Member):
			raise PermissionException(message="this user is not login !")
		self._users.pop(try_to_logout.name)
		return True
