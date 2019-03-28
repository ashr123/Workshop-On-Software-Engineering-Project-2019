from main.domain.Permission import Permissions
from .TradingSystemException import PermissionException, RegistrationExeption, \
	OpenStoreExeption
from .Guest import Guest
from .Member import Member
from .Store import Store
from typing import Union, Dict, List, Optional


class TradingSystem(object):
	_users: Dict[int, Union[Member, Guest]] = {}
	_members: List[Member] = []
	_stores: List[Store] = []

	@property
	def get_members(self):
		return TradingSystem._members

	@staticmethod
	def get_user(session_id: int) -> Union[Guest, Member]:
		return TradingSystem._users[session_id]

	@staticmethod
	def get_user_if_member(session_id: int) -> Optional[Member]:
		user: Union[Guest, Member] = TradingSystem.get_user(session_id)
		if isinstance(user, Member):
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
	def register_member(session_id: int, username: str, password: str) -> None:
		if username in map(lambda m: m.name, TradingSystem._members):
			raise RegistrationExeption(message="the user {} is already registered".format(username))
		if not isinstance(TradingSystem._users[session_id], Guest):
			raise RegistrationExeption(message="user {} already logged in".format(username))
		new_member = Member(name=username,guest=TradingSystem._users[session_id])
		TradingSystem.add_member(new_member)
		TradingSystem._users[session_id] = new_member

	@staticmethod
	def open_store(session_id: int, store_name: str, desc: str,
	               permissions_list: List[Permissions]) -> None:  # TODO take care of permissions_list
		if store_name in map(lambda s: s.get_name(), TradingSystem._stores):
			raise OpenStoreExeption("store {} already exists".format(store_name))
		user: Optional[Member] = TradingSystem.get_user_if_member(session_id)
		if not TradingSystem.is_member(user=user):
			raise OpenStoreExeption(message="you are not a member!")
		store: Store = Store(name=store_name, creator=user, description=desc)
		TradingSystem._stores.append(store)
		user.add_managment_state(is_owner=True, permissions_list=permissions_list, store=store)
		return True

	@staticmethod
	def is_member(user)->bool:
		return isinstance(user, Member)

	@staticmethod
	def login(session_id: int, username: str, password: str) -> bool:
		if username not in map(lambda m: m.name, TradingSystem._members):
			raise PermissionException(message="the user {} is not a member !".format(username))
		try_to_log_in = TradingSystem.get_user(session_id)
		if try_to_log_in is not Guest:
			raise PermissionException(message="the user {} already login !".format(username))
		new_logged_in_member: Optional[Member] = TradingSystem.get_member(member_name=username)
		if not new_logged_in_member.login(username=username, password=password):
			raise PermissionException(message="wrong password !".format(username))
		TradingSystem._users[session_id] = new_logged_in_member
		return True

	@staticmethod
	def logout(session_id: int) -> bool:
		try_to_logout: Optional[Member] = TradingSystem.get_user_if_member(session_id)
		if try_to_logout is None:
			raise PermissionException(message="this user is not logged in!")
		TradingSystem._users[session_id] = try_to_logout.get_guest()
		return True

	@staticmethod
	def add_member(new_member)->type(None):
		TradingSystem._members.append(new_member)
