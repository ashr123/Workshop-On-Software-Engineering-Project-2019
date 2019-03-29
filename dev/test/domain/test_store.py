import pytest
from main.domain.Store import Store
from main.domain.Item import Item


def test_add_item():
	store = Store(name="RoysStore", creator=None, description="nice store")
	item_id = 123
	item_name = "bamba"
	item_price = 12
	new_item = Item(id=item_id, name=item_name, price=item_price)
	store.add_item(new_item=new_item)
	assert store.has_item(new_item)


def test_remove_item():  # TODO fix
	assert False


def test_edit_item():
	assert False
