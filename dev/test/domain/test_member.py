from main.domain import Guest, Permission, Item, Member, Store, TradingSystem


def test_save_item_in_gc():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	assert not member.watch_gc()
	member.add_item_to_cart(Item.Item(0, "First item", "The first item!", "cat", 12.4, 2), "First store")
	assert member.watch_gc()


def test_add_managment_state():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	member2: Member.Member = Member.Member("Rotem", Guest.Guest())
	assert not member.stores_managed_states
	member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER], Store.Store("Second store", member, "bla bla bla"), member2)
	assert member.stores_managed_states


def test_add_manager():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	member2: Member.Member = Member.Member("Rotem", Guest.Guest())
	member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
	                           Store.Store("Second store", member, "bla bla bla"), member2)
	TradingSystem.TradingSystem.add_member(member2)
	member.add_manager("Second store", "Rotem", [Permission.Permissions.ADD_MANAGER])
	TradingSystem.TradingSystem.clear()
	assert True

def test_remove_owner():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	member2: Member.Member = Member.Member("Rotem", Guest.Guest())
	store: Store.Store = Store.Store("Second store", member2, "bla bla bla")
	member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
	                           store, member2)
	member2.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
	                           store, member)
	store.add_owner(member)
	TradingSystem.TradingSystem.add_member(member)
	TradingSystem.TradingSystem.add_member(member2)
	member2.remove_owner("Second store", "Roy")
	TradingSystem.TradingSystem.clear()
