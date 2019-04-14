from main.domain.DomainFacade import DomainFacade


class ServiceFacade(object):
	def initiateSession(self):
		return DomainFacade.initiate_session()

	def clear(self):
		DomainFacade.clear()

	def setup(self, username, password):
		ans = DomainFacade.setup(username, password)
		if ans == True:
			return "OK"
		return ans

	def register(self, sessionId, username, password):
		ans = DomainFacade.register(sessionId, username, password)
		if ans == True:
			return "OK"
		return ans

	def login(self, sessionId, username, password):
		ans = DomainFacade.login(sessionId, username, password)
		if ans == True:
			return "OK"
		return ans

	def logout(self, sessionId):
		return DomainFacade.logout(sessionId)

	def searchItem(self, name=None, category=None, hashtag=None, fil_price=None, fil_rankItem=None, fil_category=None,
	               fil_rankStore=None):
		return DomainFacade.search_item(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                fil_price=fil_price)

	def saveItemInCart(self, session_id: int, item_name: str, store_name: str):
		return DomainFacade.add_item_to_cart(session_id, item_name, store_name)

	def watchCart(self, sessionId):
		return DomainFacade.watch_cart(sessionId)

	def removeItemFromCart(self, session_id, item_name: str, store_name: str):
		return DomainFacade.remove_item_from_cart(session_id, item_name, store_name)

	def changeItemQuantityInCart(self, session_id: int, item_name: str, store_name: str, quantity: int):
		return DomainFacade.change_item_quantity_in_cart(session_id, item_name, store_name, quantity)

	def buySingleItem(self, sessionId: int, store_name: str, item_name: str) -> int:
		return DomainFacade.buy_single_item(sessionId=sessionId, store_name=store_name, item_name=item_name)

	def buyManyItems(self, sessionId, store_name, items):
		return DomainFacade.buy_many_items(sessionId, store_name, items)

	def pay(self, sessionId, trans_id, creditcard, date, snum):
		return DomainFacade.pay(trans_id, creditcard, date, snum)

	def addStore(self, sessionId, name, description):
		return DomainFacade.add_store(sessionId, name, description)

	def addItemToStore(self, sessionId, storeName, itemName, category, desc, price, amount):
		return DomainFacade.add_item_to_store(sessionId, storeName, itemName, category, desc, price, amount)

	def removeItemFromStore(self, sessionId, item_id, storeName):
		return DomainFacade.remove_item_from_store(sessionId, item_id, storeName)

	def changeItemInStore(self, sessionId, item_name, store_name, field, value):
		return DomainFacade.change_item_in_store(sessionId, item_name, store_name, field, value)

	def addOwner(self, sessionId, ownerId, storeName):
		return DomainFacade.add_owner(sessionId, ownerId, storeName)

	def removeOwner(self, session_id: int, owner_name: str, store_name: str):
		return DomainFacade.remove_owner(session_id, owner_name, store_name)

	def addManager(self, sessionId: int, manager_name: str, storeName, permissions):
		return DomainFacade.add_manager(sessionId, manager_name, storeName, permissions)

	def removeManager(self, sessionId, managerId, storeName):
		return DomainFacade.remove_manager(sessionId, managerId, storeName)

	def removeMember(self, session_id: int, username: str):
		return DomainFacade.remove_member(session_id, username)

	def exit(self, sessionId):
		return DomainFacade.exit(sessionId)

	def watch_trans(self, trans_id):
		return DomainFacade.watch_trans(trans_id)

	def supply(self, sessionId, trans_id, address):
		return DomainFacade.supply(sessionId, trans_id, address)
