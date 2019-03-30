from main.domain import Guest, Permission, Item, Member, Store


def test_save_item_in_gc():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	assert not member.watch_gc()
	member.add_item_to_cart(Item.Item(0, "First item", "The first item!", "cat", 12.4, 2), "First store")
	assert member.watch_gc()


def test_add_managment_state():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	member2: Member.Member = Member.Member("Rotem", Guest.Guest())
	assert not member.stores_managed_states
	member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER], "Second store", member2)
	assert member.stores_managed_states


def test_add_manager():
	member: Member.Member = Member.Member("Roy", Guest.Guest())
	member2: Member.Member = Member.Member("Rotem", Guest.Guest())
	member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER], "Second store", member2)
	member.add_manager("Second store", "Rotem", [Permission.Permissions.ADD_MANAGER])
	assert True

