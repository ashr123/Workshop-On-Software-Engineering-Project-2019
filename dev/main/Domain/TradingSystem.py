from main.security.Security import Security
from .TradingSystemException import UserAlreadyExistException
from .Guset import Guest
from .Member import Member
from .Store import Store
from .User import User
from typing import Union, Dict, List, Optional


class TradingSystem(object):
	_users: Dict[int, Union[Member, Guest]] = {}
	_members: List[Member] = []
	_stores: List[Store] = []

	@staticmethod
	def get_user(session_id: int) -> Union[Guest, Member]:
		return TradingSystem._users[session_id]
	
	@staticmethod
	def get_user_if_member(session_id: int) -> Optional[Member]:
		user: Union[Guest, Member] = TradingSystem.get_user(session_id)
		if user is Member:
			return user

	@staticmethod
	def get_member(member_name: str) -> Optional[Member]:
		if member_name in map(lambda member: member.name, TradingSystem._members):
			return list(filter(lambda member: member.name == member_name, TradingSystem._members))[0]
		return None

	@staticmethod
	def generate_id() -> int:
		"""
		Generates new session ID
		:rtype: int
		:return: The new ID
		"""
		new_session_id: int = len(TradingSystem._users)
		TradingSystem._users[new_session_id] = Guest()
		return new_session_id

	@staticmethod
	def search(keyword):
		return False

	@staticmethod
	def register_member(session_id: int, username: str, password: str) -> bool:
		if username in map(lambda m: m.name, TradingSystem._members):
			raise UserAlreadyExistException(message="the user {} is already registered".format(username))
		if Security.contains(username):
			return False
		Security.add_user_password(username=username, password=password)
		if TradingSystem._users[session_id] is not Guest:
			return False
		TradingSystem._users[session_id] = TradingSystem._members[session_id] = Member(name=username, guest=TradingSystem._users[session_id])

	@staticmethod
	def open_store(creator: Member, name: str, desc: str):
		pass
