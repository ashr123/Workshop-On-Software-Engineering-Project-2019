import pytest

from main.service.ServiceFacade import ServiceFacade


class TestClass(object):
	def set_up(self):
		self._serviceFacade = ServiceFacade()
		self._serviceFacade.setup("rotem", "123456")

	def set_up0(self):
		self.set_up()
		id1 = self._serviceFacade.initiateSession()
		username = "noa"
		password = "098765"
		self._serviceFacade.register(id1, username, password)
		return id1

	def set_up1(self):
		id1 = self.set_up0()
		self._store_1 = {'name': 'Dogs World'}
		self._item_1 = {'name': "fur shampoo", 'store': self._store_1['name'], 'id_DEPRECATED': 0}
		self._item_2 = {'name': "fur conditioner", 'store': self._store_1['name']}
		self._item_3 = {'name': "fur mask", 'store': self._store_1['name']}
		self._serviceFacade.login(id1, "noa", "098765")
		self._serviceFacade.addStore(id1, self._store_1['name'], "Everything you need for your dog")
		self._item_1['id_DEPRECATED'] = self._serviceFacade.addItemToStore(id1, self._store_1['name'],
		                                                                   self._item_1['name'],
		                                                                   "Pets",
		                                                                   "makes dogs fur shiny and soft", 13.5, 120)
		self._item_2['id_DEPRECATED'] = self._serviceFacade.addItemToStore(id1, self._store_1['name'],
		                                                                   self._item_2['name'], "Pets",
		                                                                   "makes dogs fur shiny and soft", 12, 40)
		self._item_3['id_DEPRECATED'] = self._serviceFacade.addItemToStore(id1, self._store_1['name'], self._item_3['name'], "Pets",
		                                   "makes dogs fur shiny and soft", 40, 300)
		return id1

	def set_up2(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		self._serviceFacade.saveItemInCart(sessionId, self._item2)
		self._serviceFacade.saveItemInCart(sessionId, self._item3)
		return sessionId

	def initiateSession(self):
		return self._serviceFacade.initiateSession()

	# 1.1 setup 1
	def test_setup1(self):
		self.set_up()
		username = "rotem"
		password = "123456"
		assert "OK" == self._serviceFacade.setup(username, password)
		self._serviceFacade.clear()

	# 1.1 setup 2
	def test_setup2(self):
		self.set_up()
		username = "rotem"
		password = "12"
		assert "Password must be of length 6" == self._serviceFacade.setup(username, password)
		self._serviceFacade.clear()

	# 2.2 register 1
	def test_register1(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		username = "noa"
		password = "098765"
		assert "OK" == self._serviceFacade.register(sessionId, username, password)
		self._serviceFacade.clear()

	# 2.2 register 2
	def test_register2(self):
		self.set_up0()
		sessionId = self._serviceFacade.initiateSession()
		username = "noa"
		password = "444444"
		assert 'the user noa is already registered' == self._serviceFacade.register(sessionId, username, password)
		self._serviceFacade.clear()

	# 2.2 register 3
	def test_register3(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		username = "noa"
		password = "33"
		assert "Password must be of length 6" == self._serviceFacade.register(sessionId, username, password)
		self._serviceFacade.clear()

	# 2.3 login 1
	def test_login1(self):
		sessionId = self.set_up0()
		assert "OK" == self._serviceFacade.login(sessionId, "noa", "098765")
		self._serviceFacade.clear()

	# 2.3 login 2
	def test_login2(self):
		sessionId = self.set_up0()
		assert 'the user roi is not a member!' == self._serviceFacade.login(sessionId, "roi", "777777")
		self._serviceFacade.clear()

	# 2.3 login 3
	def test_login3(self):
		sessionId = self.set_up0()
		assert "wrong password!" == self._serviceFacade.login(sessionId, "noa", "098769")
		self._serviceFacade.clear()

	# 2.5 search 1
	def test_searchItem1(self):
		self.set_up1()
		name = "fur shampoo"
		category = None
		hashtag = None
		fil_category = None
		fil_rankItem = None
		fil_rankStore = None
		fil_price = None
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                       fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                       fil_price=fil_price)
		assert items == ["fur shampoo, makes dogs fur shiny and soft, 13.5"]
		self._serviceFacade.clear()

	# 2.5 search 2
	def test_searchItem2(self):
		self.set_up1()
		name = None
		category = None
		hashtag = None
		fil_category = None
		fil_rankItem = None
		fil_rankStore = None
		fil_price = 500
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                       fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                       fil_price=fil_price)
		assert "fur shampoo, makes dogs fur shiny and soft, 13.5" in items
		assert "fur conditioner, makes dogs fur shiny and soft, 12" in items
		assert "fur mask, makes dogs fur shiny and soft, 40" in items
		assert len(items) == 3
		self._serviceFacade.clear()

	# 2.5 search 3
	def test_searchItem3(self):
		self.set_up1()
		name = None
		category = None
		hashtag = None
		fil_category = None
		fil_rankItem = None
		fil_rankStore = None
		fil_price = -500
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                       fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                       fil_price=fil_price)
		assert items == []
		self._serviceFacade.clear()

	# 2.5 search 6
	def test_searchItem6(self):
		self.set_up1()
		name = "Panten Shampoo"
		category = None
		hashtag = None
		fil_category = None
		fil_rankItem = None
		fil_rankStore = None
		fil_price = None
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                       fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                       fil_price=fil_price)
		assert [] == items
		self._serviceFacade.clear()

	# 2.5 search 6
	def test_searchItem6(self):
		self.set_up1()
		name = None
		category = None
		hashtag = None
		fil_category = "Pets"
		fil_rankItem = None
		fil_rankStore = None
		fil_price = None
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category,
		                                       fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore,
		                                       fil_price=fil_price)
		assert "fur shampoo, makes dogs fur shiny and soft, 13.5" in items
		assert "fur conditioner, makes dogs fur shiny and soft, 12" in items
		assert "fur mask, makes dogs fur shiny and soft, 40" in items
		assert len(items) == 3
		self._serviceFacade.clear()

	# 2.6 save item 1
	def test_saveItem1(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		assert "OK" == self._serviceFacade.saveItemInCart(sessionId, self._item1)
		self._serviceFacade.clear()

	# 2.6 save item 2
	def test_saveItem2(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		assert "Dogs World: fur shampoo 2 27.0\n" == self._serviceFacade.watchCart(sessionId)
		self._serviceFacade.clear()

	# 2.6 save item 3
	def test_saveItem3(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		assert "item number -8 doesn't exist" == self._serviceFacade.saveItemInCart(sessionId, -8)
		self._serviceFacade.clear()

	# 2.7 edit cart 1 part 1
	def test_watchCart(self):
		sessionId = self.set_up2()
		assert [[["fur shampoo", 1, 13.5], ["fur conditioner", 1, 12],
		         ["fur mask", 1, 40]]] == self._serviceFacade.watchCart(sessionId)
		self._serviceFacade.clear()

	# 2.7 edit cart 1 part 2
	def test_removeItemFromCart(self):
		sessionId = self.set_up2()
		assert [["fur shampoo", 1, 13.5], ["fur mask", 1, 40]] == self._serviceFacade.removeItemFromCart(sessionId,
		                                                                                                 self._item2)
		self._serviceFacade.clear()

	# 2.7 edit cart 2
	def test_changeItemQuantityInCart(self):
		sessionId = self.set_up2()
		assert [["fur shampoo", 3, 13.5], ["fur conditioner", 1, 12],
		        ["fur mask", 1, 40]] == self._serviceFacade.changeItemQuantityInCart(sessionId, self._item1, 2)
		self._serviceFacade.clear()

	# 2.8.1 buy singel item 1
	def test_buySingleItem1_only_buy_step(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		assert self._serviceFacade.buySingleItem(sessionId, store_name=store_name, item_name=item_name) == "OK"
		self._serviceFacade.clear()

	# 2.8.1 buy singel item 1
	def test_buySingleItem1_only_pay_step(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, self._item3)
		exist = False
		if price > 0:
			exist = True
		assert exist == True
		assert self._serviceFacade.pay(sessionId, "1234123412341234", "09/20", "777",
		                               "Hakishon 12, Tel Aviv") == "OK"
		self._serviceFacade.clear()

	# 2.8.1 buy singel item 1
	def test_buySingleItem1_only_supply_step(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, self._item3)
		exist = False
		if price > 0:
			exist = True
		assert exist == True
		assert self._serviceFacade.pay(sessionId, "1234123412341234", "09/20", "777",
		                               "Hakishon 12, Tel Aviv") == "OK"
		self._serviceFacade.clear()

	# 2.8.1 buy singel item 2
	def test_buySingleItem2(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, -23333)
		exist = False
		if price > 0:
			exist = True
		assert False == exist
		self._serviceFacade.clear()

	# 2.8.1 buy singel item 3
	def test_buySingleItem3(self):
		self.set_up1()
		sessionId = self._serviceFacade.initiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, self._item2)
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "Payment failed" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/18", "777",
		                                                   "Hakishon 12, Tel Aviv")
		self._serviceFacade.clear()

	# 2.8.2 buy many items 1
	def test_buyManyItems1(self):
		sessionId = self.set_up2()
		price = self._serviceFacade.buyManyItems(sessionId, [self._item1, self._item2])
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "OK" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/20", "777", "Hakishon 12, Tel Aviv")
		self._serviceFacade.clear()

	# 2.8.2 buy many items 2
	def test_buyManyItems2(self):
		sessionId = self._serviceFacade.initiateSession()
		price = self._serviceFacade.buyManyItems(sessionId, [-22222, 667])
		exist = False
		if price > 0:
			exist = True
		assert False == exist
		self._serviceFacade.clear()

	# 2.8.2 buy many items 3
	def test_buyManyItems3(self):
		sessionId = self.set_up2()
		price = self._serviceFacade.buyManyItems(sessionId, [self._item1, self._item2])
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "Payment failed" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/18", "777",
		                                                   "Hakishon 12, Tel Aviv")
		self._serviceFacade.clear()

	# 3.1 logout 1
	def test_logout1(self):
		sessionId = self.set_up1()
		assert "OK" == self._serviceFacade.logout(sessionId)
		self._serviceFacade.clear()

	# 3.1 logout 2
	def test_logout2(self):
		sessionId = self.set_up0()
		assert "unable to logout guest" == self._serviceFacade.logout(sessionId)
		self._serviceFacade.clear()

	# 3.2 add store 1
	def test_addStore1(self):
		sessionId = self.set_up1()
		assert "OK" == self._serviceFacade.addStore(sessionId, "Cats World", "Everything you need for your cat")
		self._serviceFacade.clear()

	# 3.2 add store 2
	def test_addStore2(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		assert "Guset has no permission to open a store" == self._serviceFacade.addStore(sessionId, "Cats World",
		                                                                                 "Everything you need for your cat")
		self._serviceFacade.clear()

	# 3.2 add store 3
	def test_addStore3(self):
		sessionId = self.set_up1()
		assert 'store Dogs World already exists' == self._serviceFacade.addStore(sessionId, "Dogs World",
		                                                                         "Everything you need for your cat")
		self._serviceFacade.clear()

	# 4.1.1 add item to store 1
	def test_addItemToStore1(self):
		ownerid = self.set_up1()
		assert "OK" == self._serviceFacade.addItemToStore(ownerid, "Dogs World", "fur comb", "Pets",
		                                                  "for all kinds of fur", 4, 321)
		self._serviceFacade.clear()

	# 4.1.1 add item to store 2
	def test_addItemToStore2(self):
		ownerid = self.set_up1()
		assert "you don't have permissions to add item to store" == self._serviceFacade.addItemToStore(ownerid + 1,
		                                                                                               "Dogs World",
		                                                                                               "fur comb",
		                                                                                               "Pets",
		                                                                                               "for all kinds of fur",
		                                                                                               4, 321)
		self._serviceFacade.clear()

	# 4.1.2 remove item from store 1 ok
	def test_removeItemFromStore1(self):
		ownerid = self.set_up1()
		assert self._serviceFacade.removeItemFromStore(ownerid, self._item1, "Dogs World") == "OK"
		self._serviceFacade.clear()

	# 4.1.2 remove item from store 2 not good
	def test_removeItemFromStore2(self):
		ownerid = self.set_up1()
		assert self._serviceFacade.removeItemFromStore(ownerid, -9, "Dogs World") == "Item not exist in store"
		self._serviceFacade.clear()

	# 4.1.3 edit item in store 1 ok
	def test_changeItemInStore1(self):
		ownerid = self.set_up1()
		assert self._serviceFacade.removeItemFromStore(ownerid, self._item1, "Dogs World", "price", 17) == "OK"
		self._serviceFacade.clear()

	# 4.1.3 edit item in store 2
	def test_changeItemInStore2(self):
		ownerid = self.set_up1()
		assert self._serviceFacade.changeItemInStore(ownerid + 1, self._item1, "Dogs World", "price", 17) == "OK"
		self._serviceFacade.clear()

	# 4.3 add owner 1
	def test_addOwner1(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		assert "OK" == self._serviceFacade.addOwner(sessionId, username, "Dogs World")
		self._serviceFacade.clear()

	# 4.3 add owner 2
	def test_addOwner2(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		assert "guest can't nominate owners" == self._serviceFacade.addOwner(sessionId, "rotem", "Dogs World")
		self._serviceFacade.clear()

	# 4.3 add owner 3
	@pytest.mark.skip(reason="no way of currently testing this")
	def test_addOwner3(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		assert "guest can't be nominate as an owner" == self._serviceFacade.addOwner(sessionId, ownerId, "Dogs World")
		self._serviceFacade.clear()

	# 4.3 add owner 4
	def test_addOwner4(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, username, "Dogs World")
		assert "circular nomination" in self._serviceFacade.addOwner(ownerId, "noa", "Dogs World")
		self._serviceFacade.clear()

	# 4.4 remove owner 1
	def test_removeOwner1(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, username, "Dogs World")
		assert "OK" == self._serviceFacade.removeOwner(sessionId, username, "Dogs World")
		self._serviceFacade.clear()

	# 4.4 remove owner 2
	def test_removeOwner2(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, username, "Dogs World")
		ownerId1 = self._serviceFacade.initiateSession()
		username1 = "ofer"
		password1 = "777777"
		self._serviceFacade.register(ownerId1, username1, password1)
		self._serviceFacade.login(ownerId1, username1, password1)
		self._serviceFacade.addOwner(sessionId, username1, "Dogs World")
		assert "owner can't remove another owner that he didn't nominate" == self._serviceFacade.removeOwner(ownerId,
		                                                                                                     username1,
		                                                                                                     "Dogs World")
		self._serviceFacade.clear()

	# 4.5 add manager 1
	def test_addManager1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		assert "OK" == self._serviceFacade.addManager(sessionId, username, "Dogs World", ["REMOVE_ITEM"])
		self._serviceFacade.clear()

	# 4.5 add manager 2
	def test_addManager2(self):
		self.set_up()
		sessionId = self._serviceFacade.initiateSession()
		managerId = self._serviceFacade.initiateSession()
		assert "guest can't nominate managers" == self._serviceFacade.addManager(sessionId, managerId, "Dogs World",
		                                                                         ["ADD_ITEM"])
		self._serviceFacade.clear()

	# 4.6 remove manager 1
	def test_removeManager1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.login(managerId, username, password)
		self._serviceFacade.addManager(sessionId, username, "Dogs World", ["REMOVE_ITEM", "ADD_ITEM"])
		assert "OK" == self._serviceFacade.removeManager(sessionId, username, "Dogs World")
		self._serviceFacade.clear()

	# 4.6 remove manager 2
	def test_removeManager2(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, username, "Dogs World")
		managerId = self._serviceFacade.initiateSession()
		username1 = "ofer"
		password1 = "777777"
		self._serviceFacade.register(managerId, username1, password1)
		self._serviceFacade.login(managerId, username1, password1)
		self._serviceFacade.addManager(sessionId, username1, "Dogs World", [])
		assert "manager can't remove another manager that he didn't nominate" == self._serviceFacade.removeManager(
			ownerId,
			username1,
			"Dogs World")
		self._serviceFacade.clear()

	# 5.1 manager tries to remove item 1
	def test_managerDoingThings1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.login(managerId, username, password)
		self._serviceFacade.addManager(sessionId, username, "Dogs World", ["ADD_ITEM", "REMOVE_ITEM", "EDIT_ITEM"])
		assert "OK" == self._serviceFacade.removeItemFromStore(managerId, self._item_1['id_DEPRECATED'], "Dogs World")
		self._serviceFacade.clear()

	# 5.1 manager tries to remove item 2
	def test_managerDoingThings2(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.login(managerId, username, password)
		self._serviceFacade.addManager(sessionId, username, "Dogs World", ["EDIT_ITEM", "ADD_ITEM"])
		assert "you don't have the permission to do this action!" == self._serviceFacade.removeItemFromStore(managerId,
		                                                                                                     self._item_1[
			                                                                                                     'id_DEPRECATED'],
		                                                                                                     "Dogs World")
		self._serviceFacade.clear()

	# 5.1 manager tries to remove item 3
	def test_managerDoingThings3(self):
		sessionId = self.set_up1()
		guestId = self._serviceFacade.initiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(guestId, username, password)
		assert "guest can't remove item from store" == self._serviceFacade.removeItemFromStore(guestId, self._item_1[
			'id_DEPRECATED'],
		                                                                                       "Dogs World")
		self._serviceFacade.clear()

	# 6.3 remove user 1
	def test_removeUser1(self):
		sessionid = self.set_up0()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "OK" == self._serviceFacade.removeUser(sysmanager, sessionid)
		self._serviceFacade.clear()

	# 6.3 remove user 2
	def test_removeUser2(self):
		sessionid = self.set_up1()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "OK" == self._serviceFacade.removeUser(sysmanager, sessionid)
		self._serviceFacade.clear()

	# 6.3 remove user 3
	def test_removeUser3(self):
		sessionid = self._serviceFacade.initiateSession()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "Fail: you are trying to remove a non member user" == self._serviceFacade.removeUser(sysmanager,
		                                                                                            sessionid)
		self._serviceFacade.clear()
