import pytest
from main.domain import TradingSystem
from main.domain import DomainFacade
from main.domain import Guest
from main.domain import Store
from main.domain import GroceryCart
from main.domain import Item

store_name1 = "TEST_store_roy"
item_name1 = "TEST_bamba"
store_name2 = "TEST_store_rotem"
item_name2 = "TEST_bisli"

def setup_function(function):
	facade = DomainFacade.DomainFacade()
	session_id = facade.initiate_session()
	facade.register(session_id, "TEST_store_owner", "123456")
	facade.login(session_id, "TEST_store_owner", "123456")
	facade.add_store(session_id=session_id, name=store_name1, desc="nice_store")
	facade.add_item_to_store(session_id=session_id, store_name=store_name1, item_name=item_name1, category="category",
	                         desc="nice product", price=12, amount=1)
	facade.add_store(session_id=session_id, name=store_name2, desc="nice_store")
	facade.add_item_to_store(session_id=session_id, store_name=store_name1, item_name=item_name2, category="category",
	                         desc="nice product", price=16, amount=1)
def teardown_function(function):
	TradingSystem.TradingSystem.clear()

def test_add_item_to_cart():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	store: Store.Store = TradingSystem.TradingSystem.get_store(store_name1)
	item = store.get_item_by_name(item_name1)
	assert guest.add_item_to_cart(item=item, store_name=store_name1)
	assert guest.has_item_in_cart(item_name=item_name1, store_name=store_name1)


def test_remove_item_from_cart():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	store: Store.Store = TradingSystem.TradingSystem.get_store(store_name1)
	item = store.get_item_by_name(item_name1)
	guest.add_item_to_cart(item=item, store_name=store_name1)
	assert guest.remove_item_from_cart(item=item, store_name=store_name1)
	assert guest.has_item_in_cart(item_name=item_name1, store_name=store_name1) is False


@pytest.mark.skip(reason="no way of currently testing this, involving other classes")
def test_watch_gc():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	store: Store.Store = TradingSystem.TradingSystem.get_store(store_name1)
	item1 = store.get_item_by_name(item_name1)
	item2 = store.get_item_by_name(item_name2)
	guest.add_item_to_cart(item=item1, store_name=store_name1)
	guest.add_item_to_cart(item=item2, store_name=store_name2)
	assert guest.to_string_basket() == 'TEST_store_roy: TEST_bamba 1 12\nTEST_store_rotem: TEST_bisli 1 16\n'


def test_change_item_quantity_in_cart():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	store: Store.Store = TradingSystem.TradingSystem.get_store(store_name1)
	item = store.get_item_by_name(item_name1)
	guest.add_item_to_cart(item=item, store_name=store_name1)
	guest.add_item_to_cart(item=item, store_name=store_name1)
	assert guest.check_quantity(item, store_name1) == 2

def test_register1():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	assert guest.register("lala", "ererer") is True

def test_register2():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	guest.register("lala", "ererer")
	session_id2 = TradingSystem.TradingSystem.generate_id()
	guest2: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id2)
	assert guest2.register("lala", "ererer") is False

def test_login1():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	guest.register("lala", "ererer")
	assert guest.login("lala", "ererer") is True

def test_login2():
	session_id = TradingSystem.TradingSystem.generate_id()
	guest: Guest.Guest = TradingSystem.TradingSystem.get_user(session_id)
	guest.register("lala", "ererer")
	assert guest.login("lala", "ereret") is False






