from main.domain.DomainFacade import DomainFacade


class Sercive(object):

	def __init__(self):
		self._domainFacade = DomainFacade()

	def initiateSession(self):
		return self._domainFacade.intiateSession()

	def register(self, sessionId, username, password):
		return self._domainFacade.register(sessionId, username, password)

	def login(self, sessionId, username, password):
		return self._domainFacade.login(sessionId, username, password)

	def logout(self):
		return self._domainFacade.logout(sessionId)

	def searchItem(self, name=None, category=None, hashtag=None, fil_range=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return self._domainFacade.logout(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                 fil_rankItem=fil_rankItem)

	def saveItem(self, sessionId, id):
		return self._domainFacade.save_item(sessionId, id)

	def watchCart(self, sessionId):
		return self._domainFacade.watch_cart(sessionId)

	def removeItemFromCart(self, sessionId, id):
		return self._domainFacade.removeItemFromCart(sessionId, id)

	def changeItemQuantityInCart(self, sessionId, id, quantity):
		return self._domainFacade.changeItemQuantityInCart(sessionId, id, quantity)

	def buySingleItem(self, sessionId, id, paymentMethod):
		return self._domainFacade.buySingleItem(sessionId, id, paymentMethod)

	def buyManyItems(self, sessionId, ids, paymentMethod):
		return self._domainFacade.buyManyItems(sessionId, ids, paymentMethod)

	def pay(self, sessionId, payemnt_details, address):
		return self._domainFacade.pay(sessionId, payemnt_details, address)

	def addStore(self, sessionId, name):
		return self._domainFacade.add_store(sessionId, name)

	def addItemToStore(self, sessionId, storeId):
		return self._domainFacade.add_item_to_store(sessionId, storeId)

	def removeItemFromStore(self, sessionIs, id, storeId):
		return self._domainFacade.remove_item_from_store(sessionIs, id, storeId)

	def changeItemInStore(self, sessionId, id, storeId, field, value):
		return self._domainFacade.change_item_in_store(sessionId, id, storeId, field, value)

	def addOwner(self, sessionId,ownerId, storeId):
		return self._domainFacade.add_owner(sessionId, ownerId, storeId)

	def removeOwner(self, sessionId,ownerId, storeId):
		return self._domainFacade.remove_owner(sessionId, ownerId, storeId)

	def addManager(self, sessionId,ownerId, storeId, permissions):
		return self._domainFacade.add_manager(self, sessionId, ownerId, storeId, permissions)

	def removeManager(self, sessionId,ownerId, storeId):
		return self._domainFacade.remove_manager(sessionId, ownerId, storeId)

	def removeUser(self, sesesionId,id):
		return self._domainFacade.remove_user(sesesionId, id)

	def setup(self, masteruser, password):
		return self._domainFacade.setup(masteruser, password)

	def exit(self):
		return self._domainFacade.exit()
