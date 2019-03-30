import pytest
from main.domain import TradingSystem
from main.domain import DomainFacade
from main.domain import Guest
from main.domain import Store
from main.domain import Item

store_name = "TEST_store_roy"
item_name = "TEST_bamba"
def setup_module(module):
	facade = DomainFacade.DomainFacade()
	session_id = facade.initiate_session()
	facade.register(session_id, "TEST_store_owner", "123456")
	facade.login(session_id, "TEST_store_owner", "123456")
	facade.add_store(session_id=session_id,name=store_name,desc="nice_store")
	facade.add_item_to_store(session_id=session_id,store_name=store_name,itemName=item_name,category="category",
	                         desc="nice product", price=12,amount=1)


def test_add_item_to_cart():
	facade = DomainFacade.DomainFacade()
	session_id = facade.initiate_session()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	store:Store.Store = TradingSystem.TradingSystem.get_store(store_name)
	item = store.get_item_by_name(item_name)
	assert guest.add_item_to_cart(item=item,store_name=store_name)
	assert guest.has_item_in_cart(item_name=item_name,store_name=store_name)

def test_remove_item_from_cart():
	assert False

def test_watch_gc():
	assert False








