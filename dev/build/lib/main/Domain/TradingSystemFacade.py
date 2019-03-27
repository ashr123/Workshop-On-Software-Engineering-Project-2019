from main.Domain.TradingSystem import TradingSystem
from main.Domain import Member
from main.Domain.TradingSystemException import *

from dev.main.Domain.TradingSystemException import UserAlreadyExistException


class TradingSystemFacade(object):
	def __init__(self):
		# self._tradingSystem = None
		self._tradingSystem = TradingSystem()  # TODO

	def initateSession(self):
		return self._tradingSystem.generate_id()

	def login(self, username, password):
		return False

	def logout(self):
		return False

	def register(self, sessionId, username, password):
		try:
			self._tradingSystem.register_member(sessionId, username, password)
			return True
		except UserAlreadyExistException as e:
			return False

	def searchItem(self, name=None, category=None, hashtag=None, fil_range=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return False

	def saveItem(self, id):
		return False

	def watchCart(self, sessionId):
		user = self._tradingSystem.get_user(sessionId)
		return user.watchGC()

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

	def addStore(self, sessionId, name, desc):
		try:
			member = self._tradingSystem.getUser(sessionId)
			if not isinstance(member, Member):
				raise GusetCannotOpenStoreException()
			member.openStore()
		except UserAlreadyHasStoreException as e:
			return False
		except GusetCannotOpenStoreException as e:
			return False

	def addItemToStore(self, storeId, itemName, desc, price, amount):
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

	def addItemToCart(self, sessionId, itemId):
		pass

	def openStore(self, ownerSession, param):
		pass
