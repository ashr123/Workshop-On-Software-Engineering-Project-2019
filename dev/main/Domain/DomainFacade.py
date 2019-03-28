from .TradingSystem import TradingSystem
from .Member import Member
from .TradingSystemException import *
from main.Domain import Store


class DomainFacade(object):
	def initateSession(self):
		return TradingSystem.generate_id()

	def login(self, sessionId, username, password):
		try:
			TradingSystem.login(sessionId, username, password)
			return True
		except PermissionException as e:
			return False

	def logout(self, sessionId):
		try:
			TradingSystem.logout(sessionId)
			return True
		except PermissionException as e:
			return False

	def register(self, sessionId, username, password):
		try:
			TradingSystem.register_member(sessionId, username, password)
			return True
		except RegistrationExeption as e:
			return False

	def searchItem(self, name=None, category=None, hashtag=None, fil_range=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return False

	def saveItem(self, id):
		return False

	def watchCart(self, sessionId):
		user = TradingSystem.get_user(sessionId)
		return user.watch_gc()

	def removeItemFromCart(self, id):
		return False

	def changeItemQuantityInCart(self, id):
		return False

	def buySingleItem(self, id):
		return False

	def buyItemFromCart(self, ids):
		return False

	def pay(self, payemnt_details, address):
		return False

	def add_store(self, session_id: int, name: str, desc: str) -> bool:
		try:
			member: Member = TradingSystem.get_user_if_member(session_id)
			if member is None:
				raise GuestCannotOpenStoreException("User {} has no permission to open a store".format(name))
			if member.open_store(session_id=session_id,store_name=name, desc=desc):
				return True
		except UserAlreadyHasStoreException as e:
			return False
		except GuestCannotOpenStoreException as e:
			return False

	def addItemToStore(self, sessionId: int, storeId: str, itemName: str, desc: str, price: float, amount: int) -> bool:
		return False

	def removeItemFromStore(self, id, storeId):
		return False

	def changeItemInStore(self, id, storeId, field, value):
		return False

	def addOwner(self, ownerId, storeId):
		return False

	def removeOwner(self, ownerId, storeId):
		return False

	def addManager(self, ownerId, storeId, permissions):
		return False

	def removeManager(self, ownerId, storeId):
		return False

	def removeUser(self, id):
		return False

	def setup(self, masteruser, password):
		return False

	def addItemToCart(self, sessionId: int, itemName: str, storeId: str):
		pass

	def openStore(self, ownerSession, param):
		pass

	def get_member(self, session_id: int) -> Member:
		return TradingSystem.get_user(session_id)

	def get_store(self, session_id: int, store_name: str) -> Store:
		member = TradingSystem.get_user_if_member(session_id)
		if member == None:
			return None
		store_indicator = list(filter(lambda ms: ms.store.name == store_name, member.stores_managed_states))
		if len(store_indicator) == 0:
			return None
		return store_indicator[0].store
