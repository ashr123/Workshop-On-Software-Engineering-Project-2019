from main.service.ServiceFacade import ServiceFacade


class TestClass(object):
	def set_up(self):
		self._serviceFacade = ServiceFacade()
		self._serviceFacade.setup("rotem", "123456")

	def set_up0(self):
		self.set_up()
		id1 = self._serviceFacade.intiateSession()
		username = "noa"
		password = "098765"
		self._serviceFacade.register(id1, username, password)
		return id1

	def set_up1(self):
		id1= self.set_up0()
		self._serviceFacade.login(id1, "noa", "098765")
		self._serviceFacade.addStore(id1, "Dogs World", "Everything you need for your dog")
		self._item1 = self._serviceFacade.addItemToStore(id1, "Dogs World", "fur shampoo", "Pets", "makes dogs fur shiny and soft", 13.5, 120)
		self._item2 = self._serviceFacade.addItemToStore(id1, "Dogs World", "fur conditioner", "Pets", "makes dogs fur shiny and soft", 12, 40)
		self._item3 = self._serviceFacade.addItemToStore(id1, "Dogs World", "fur mask", "Pets", "makes dogs fur shiny and soft", 40, 300)
		return id1


	def set_up2(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		self._serviceFacade.saveItemInCart(sessionId, self._item2)
		self._serviceFacade.saveItemInCart(sessionId, self._item3)
		return sessionId

	def initiateSession(self):
		return self._serviceFacade.intiateSession()

	# 1.1 setup 1
	def test_setup1(self):
		self.set_up()
		username = "rotem"
		password = "123456"
		assert "OK" == self._serviceFacade.setup(username, password)

	# 1.1 setup 2
	def test_setup2(self):
		username = "rotem"
		password = "12"
		assert "password must have 6 alpha-numeric characters" == self._serviceFacade.setup(username, password)

	# 2.2 register 1
	def test_register1(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		username = "noa"
		password = "098765"
		assert "OK" == self._serviceFacade.register(sessionId, username, password)

	# 2.2 register 2
	def test_register2(self):
		self.set_up0()
		sessionId = self._serviceFacade.intiateSession()
		username = "noa"
		password = "444444"
		assert "username already taken" == self._serviceFacade.register(sessionId, username, password)

	# 2.2 register 3
	def test_register3(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		username = "noa"
		password = "33"
		assert "password must have 6 alpha-numeric characters" == self._serviceFacade.register(sessionId, username, password)


	# 2.3 login 1
	def test_login1(self):
		sessionId = self.set_up0()
		assert "OK" == self._serviceFacade.login(sessionId, "noa", "098765")

	# 2.3 login 2
	def test_login2(self):
		sessionId = self.set_up0()
		assert "unknown user" == self._serviceFacade.login(sessionId, "roi", "777777")

	# 2.3 login 3
	def test_login3(self):
		sessionId = self.set_up0()
		assert "password is incorrect" == self._serviceFacade.login(sessionId, "noa", "098769")


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
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category, fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore, fil_price=fil_price)
		assert [["fur shampoo", "makes dogs fur shiny and soft", 13.5]] == items

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
		assert [["fur shampoo", "makes dogs fur shiny and soft", 13.5],["fur conditioner",
		                                             "makes dogs fur shiny and soft", 12],["fur mask",
		                                             "makes dogs fur shiny and soft", 40]] == items

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
		assert None == items


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
		items = self._serviceFacade.searchItem(name=name, category=category, hashtag=hashtag, fil_category=fil_category, fil_rankItem=fil_rankItem, fil_rankStore=fil_rankStore, fil_price=fil_price)
		assert [["fur shampoo", "makes dogs fur shiny and soft", 13.5],["fur conditioner",
		                                             "makes dogs fur shiny and soft", 12],["fur mask",
		                                             "makes dogs fur shiny and soft", 40]] == items

	# 2.6 save item 1
	def test_saveItem1(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		assert "OK" == self._serviceFacade.saveItemInCart(sessionId, self._item1)

	# 2.6 save item 2
	def test_saveItem2(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		self._serviceFacade.saveItemInCart(sessionId, self._item1)
		assert [[["fur shampoo", 2, 27]]]== self._serviceFacade.watchCart(sessionId)

	# 2.6 save item 3
	def test_saveItem3(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		assert "Item doesn't exist" == self._serviceFacade.saveItemInCart(sessionId, -8)

	#2.7 edit cart 1 part 1
	def test_watchCart(self):
		sessionId = self.set_up2()
		assert [[["fur shampoo", 1, 13.5], ["fur conditioner", 1, 12],["fur mask", 1, 40]]] == self._serviceFacade.watchCart(sessionId)

	#2.7 edit cart 1 part 2
	def test_removeItemFromCart(self):
		sessionId = self.set_up2()
		assert [["fur shampoo", 1, 13.5],["fur mask", 1, 40]] == self._serviceFacade.removeItemFromCart(sessionId, self._item2)


	#2.7 edit cart 2
	def test_changeItemQuantityInCart(self):
		sessionId = self.set_up2()
		assert [["fur shampoo", 3, 13.5],["fur conditioner", 1, 12],["fur mask", 1, 40]] == self._serviceFacade.changeItemQuantityInCart(sessionId, self._item1, 2)

	#2.8.1 buy singel item 1
	def test_buySingleItem1(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, self._item3)
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "OK" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/20", "777", "Hakishon 12, Tel Aviv")

	#2.8.1 buy singel item 2
	def test_buySingleItem2(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, -23333)
		exist = False
		if price > 0:
			exist = True
		assert False == exist

	#2.8.1 buy singel item 3
	def test_buySingleItem3(self):
		self.set_up1()
		sessionId = self._serviceFacade.intiateSession()
		price = self._serviceFacade.buySingleItem(sessionId, self._item2)
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "Payment failed" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/18", "777", "Hakishon 12, Tel Aviv")

	#2.8.2 buy many items 1
	def test_buyManyItems1(self):
		sessionId = self.set_up2()
		price = self._serviceFacade.buyManyItems(sessionId, [self._item1, self._item2])
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "OK" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/20", "777", "Hakishon 12, Tel Aviv")

	#2.8.2 buy many items 2
	def test_buyManyItems2(self):
		sessionId = self._serviceFacade.intiateSession()
		price = self._serviceFacade.buyManyItems(sessionId, [-22222, 667])
		exist = False
		if price > 0:
			exist = True
		assert False == exist

	#2.8.2 buy many items 3
	def test_buyManyItems3(self):
		sessionId = self.set_up2()
		price = self._serviceFacade.buyManyItems(sessionId, [self._item1, self._item2])
		exist = False
		if price > 0:
			exist = True
		assert True == exist
		assert "Payment failed" == self._serviceFacade.pay(sessionId, "1234123412341234", "09/18", "777", "Hakishon 12, Tel Aviv")

	# 3.1 logout 1
	def test_logout1(self):
		sessionId = self.set_up1()
		assert "OK" == self._serviceFacade.logout(sessionId)

	# 3.1 logout 2
	def test_logout2(self):
		sessionId = self.set_up0()
		assert "unable to logout guest" == self._serviceFacade.logout(sessionId)

	# 3.2 add store 1
	def test_addStore1(self):
		sessionId = self.set_up1()
		assert "OK" == self._serviceFacade.addStore(sessionId, "Cats World", "Everything you need for your cat")

	# 3.2 add store 2
	def test_addStore2(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		assert "guest can't open a store" == self._serviceFacade.addStore(sessionId, "Cats World", "Everything you need for your cat")

	# 3.2 add store 3
	def test_addStore3(self):
		sessionId = self.set_up1()
		assert "the store name is already taken" == self._serviceFacade.addStore(sessionId, "Dogs World", "Everything you need for your cat")

	# 4.1.1 add item to store 1
	def test_addItemToStore1(self):
		ownerid = self.set_up1()
		assert "OK" == self._serviceFacade.addItemToStore(ownerid, "Dogs World", "fur comb", "Pets", "for all kinds of fur", 4, 321)

	# 4.1.1 add item to store 2
	def test_addItemToStore2(self):
		ownerid = self.set_up1()
		assert "you don't have permissions to add item to store" == self._serviceFacade.addItemToStore(ownerid + 1, "Dogs World", "fur comb", "Pets", "for all kinds of fur", 4, 321)

	# 4.1.2 remove item from store 1
	def test_removeItemFromStore1(self):
		ownerid = self.set_up1()
		return self._serviceFacade.removeItemFromStore(ownerid, self._item1, "Dogs World")

	# 4.1.2 remove item from store 2
	def test_removeItemFromStore2(self):
		ownerid = self.set_up1()
		return self._serviceFacade.removeItemFromStore(ownerid, -9, "Dogs World")

	# 4.1.3 edit item in store 1
	def test_changeItemInStore1(self):
		ownerid = self.set_up1()
		return self._serviceFacade.removeItemFromStore(ownerid, self._item1, "Dogs World", "price", 17)

	# 4.1.3 edit item in store 2
	def test_changeItemInStore2(self):
		ownerid = self.set_up1()
		return self._serviceFacade.changeItemInStore(ownerid + 1, self._item1, "Dogs World", "price", 17)

	# 4.3 add owner 1
	def test_addOwner1(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		assert "OK" == self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")

	# 4.3 add owner 2
	def test_addOwner2(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		ownerId = self._serviceFacade.intiateSession()
		assert "guest can't nominate owners" == self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")

	# 4.3 add owner 3
	def test_addOwner3(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		assert "guest can't be nominate as an owner" == self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")

	# 4.3 add owner 4
	def test_addOwner4(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")
		assert "circular nomination" == self._serviceFacade.addOwner(ownerId, sessionId, "Dogs world")

	# 4.4 add owner 1
	def test_removeOwner1(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")
		assert "OK" == self._serviceFacade.removeOwner(sessionId, ownerId, "Dogs world")

	# 4.4 add owner 2
	def test_removeOwner2(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")
		ownerId1 = self._serviceFacade.intiateSession()
		username1 = "ofer"
		password1 = "777777"
		self._serviceFacade.register(ownerId1, username1, password1)
		self._serviceFacade.login(ownerId1, username1, password1)
		self._serviceFacade.addOwner(sessionId, ownerId1, "Dogs world")
		assert "owner can't remove another owner that he didn't nominate" == self._serviceFacade.removeOwner(ownerId, ownerId1, "Dogs world")

	# 4.5 add manager 1
	def test_addManager1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		assert "OK" == self._serviceFacade.addManager(sessionId, managerId, "Dogs world", [1])

	# 4.5 add manager 2
	def test_addManager2(self):
		self.set_up()
		sessionId = self._serviceFacade.intiateSession()
		managerId = self._serviceFacade.intiateSession()
		assert "guest can't nominate manager" == self._serviceFacade.addManager(sessionId, managerId, "Dogs world", [2])

	# 4.6 remove manager 1
	def test_removeManager1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.login(managerId, username, password)
		self._serviceFacade.addManager(sessionId, managerId, "Dogs world", [1, 2])
		assert "OK" == self._serviceFacade.removeManager(sessionId, managerId, "Dogs world")

	# 4.6 remove manager 2
	def test_removeManager2(self):
		sessionId = self.set_up1()
		ownerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(ownerId, username, password)
		self._serviceFacade.login(ownerId, username, password)
		self._serviceFacade.addOwner(sessionId, ownerId, "Dogs world")
		managerId = self._serviceFacade.intiateSession()
		username1 = "ofer"
		password1 = "777777"
		self._serviceFacade.register(managerId, username1, password1)
		self._serviceFacade.login(managerId, username1, password1)
		self._serviceFacade.addManager(sessionId, managerId, "Dogs world")
		assert "owner can't remove manager that he didn't nominate" == self._serviceFacade.removeManager(ownerId, managerId, "Dogs world")


	#5.1 manager tries to remove item 1
	def test_managerDoingThings1(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.addManager(sessionId, managerId, "Dogs world", [1, 2, 3])
		assert "OK" == self._serviceFacade.removeItemFromStore(sessionId, self._item1, "Dogs World")

	# 5.1 manager tries to remove item 2
	def test_managerDoingThings2(self):
		sessionId = self.set_up1()
		managerId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(managerId, username, password)
		self._serviceFacade.addManager(sessionId, managerId, "Dogs world", [1, 2])
		assert "manager doesn't have the permissions" == self._serviceFacade.removeItemFromStore(sessionId, self._item1, "Dogs World")

	# 5.1 manager tries to remove item 3
	def test_managerDoingThings3(self):
		sessionId = self.set_up1()
		guestId = self._serviceFacade.intiateSession()
		username = "dana"
		password = "666666"
		self._serviceFacade.register(guestId, username, password)
		assert "guest can't remove item from store" == self._serviceFacade.removeItemFromStore(guestId, self._item1, "Dogs World")

	# 6.3 remove user 1
	def test_removeUser1(self):
		sessionid = self.set_up0()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "OK" == self._serviceFacade.removeUser(sysmanager, sessionid)

	# 6.3 remove user 2
	def test_removeUser2(self):
		sessionid = self.set_up1()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "OK" == self._serviceFacade.removeUser(sysmanager, sessionid)

	# 6.3 remove user 3
	def test_removeUser3(self):
		sessionid = self._serviceFacade.initiateSession()
		sysmanager = self._serviceFacade.initiateSession()
		self._serviceFacade.login(sysmanager, "rotem", "123456")
		assert "Fail: you are trying to remove a non member user" == self._serviceFacade.removeUser(sysmanager, sessionid)

