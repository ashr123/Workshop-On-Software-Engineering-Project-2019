from main.Domain.TradingSystem import TradingSystem


class Facade(object):
	def __init__(self):
		pass

	def login(self, username, password):
		return False

	def logout(self):
		return False

	def register(self, username, password):
		return False

	def searchItem(self, name=None, category=None, hashtag=None, fil_range=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return False

	def saveItem(self, id):
		return False

	def watchCart(self):
		return False

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

	def addStore(self, name, desc):
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
