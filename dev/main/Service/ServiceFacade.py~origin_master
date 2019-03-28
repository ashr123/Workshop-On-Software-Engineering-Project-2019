from main.Domain.TradingSystemFacade import TradingSystemFacade


class ServiceFacade(object):

	def __init__(self):
		self._domainFacade = TradingSystemFacade()

	def initiateSession(self):
		return self._domainFacade.intiateSession()

	def setup(self, username, password):
		return self._domainFacade.setup(username, password)

	def register(self, sessionId, username, password):
		return self._domainFacade.register(sessionId, username, password)

	def login(self, sessionId, username, password):
		return self._domainFacade.login(sessionId, username, password)

	def logout(self, sessionId):
		return self._domainFacade.logout(sessionId)

	def searchItem(self, name=None, category=None, hashtag=None, fil_price=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return self._domainFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                 fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore, fil_price=fil_price)

	def saveItemInCart(self, sessionId, id):
		return self._domainFacade.saveItem(sessionId, id)

	def watchCart(self, sessionId):
		return self._domainFacade.watchCart(sessionId)

	def removeItemFromCart(self, sessionId, id):
		return self._domainFacade.removeItemFromCart(sessionId, id)

	def changeItemQuantityInCart(self, sessionId, id, quantity):
		return self._domainFacade.changeItemQuantityInCart(sessionId, id, quantity)

	def buySingleItem(self, sessionId, id):
		return self._domainFacade.buySingleItem(sessionId, id)

	def buyManyItems(self, sessionId, ids):
		return self._domainFacade.buyManyItems(sessionId, ids)

	def pay(self, sessionId, creditcard, date, snum,  address):
		return self._domainFacade.pay(sessionId, creditcard, date, snum,  address)

	def addStore(self, sessionId, name, description):
		return self._domainFacade.addStore(sessionId, name, description)

	def addItemToStore(self, sessionId, storeName, itemName, category, desc, price, amount):
		return self._domainFacade.addItemToStore(sessionId, storeName, itemName, category, desc, price, amount)

	def removeItemFromStore(self, sessionIs, id, storeName):
		return self._domainFacade.removeItemFromStore(sessionIs, id, storeName)

	def changeItemInStore(self, sessionId, id, storeName, field, value):
		return self._domainFacade.changeItemInStore(sessionId, id, storeName, field, value)

	def addOwner(self, sessionId, ownerId, storeName):
		return self._domainFacade.addOwner(sessionId,ownerId, storeName)

	def removeOwner(self, sessionId, ownerId, storeName):
		return self._domainFacade.removeOwner(sessionId,ownerId, storeName)

	def addManager(self, sessionId, managerId, storeName, permissions):
		return self._domainFacade.addManager(self, sessionId, managerId, storeName, permissions)

	def removeManager(self, sessionId, managerId, storeName):
		return self._domainFacade.removeManager(sessionId,managerId, storeName)

	def removeUser(self, sessionId, id):
		return self._domainFacade.removeUser(sessionId, id)

	def exit(self, sessionId):
		return self._domainFacade.exit(sessionId)

