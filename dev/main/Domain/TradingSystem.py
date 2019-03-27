from .TradingSystemException import UserAlreadyExistException
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
