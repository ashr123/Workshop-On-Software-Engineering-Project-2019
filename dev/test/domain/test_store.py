from main.domain import Store
from main.domain import Item


def test_add_item():
	store = create_store_instance()
	new_item = create_item_instance()
	store.add_item(new_item=new_item)
	assert store.has_item(new_item.id)


def test_remove_item():
	store = create_store_instance()
	new_item = create_item_instance()
	store.add_item(new_item=new_item)
	assert store.has_item(new_item.id)
	store.remove_item(item_id=new_item.id)
	assert not store.has_item(new_item.id)


def test_edit_item():
	store = create_store_instance()
	new_item = create_item_instance()
	store.add_item(new_item=new_item)
	new_name = "NEW_ITEM_NAME_WIII"
	new_price = 14
	assert store.edit_item(item_id=new_item.id, new_name=new_name, new_price=new_price)
	edited_item: Item = store.get_item(new_item.id)
	assert edited_item.name == new_name
	assert edited_item.price == new_price


def create_store_instance() -> Store.Store:
	return Store.Store(name="RoysStore", creator=None, description="nice store")


def create_item_instance() -> Item.Item:
	item_id = 123
	item_name = "bamba"
	item_price = 12
	return Item.Item(id=item_id, name=item_name, price=item_price, description="Nice Bamba", category="Food",
	                 quantity=666)
