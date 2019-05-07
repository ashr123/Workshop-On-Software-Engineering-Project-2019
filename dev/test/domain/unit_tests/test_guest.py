import pytest

from main.domain.Guest import Guest
from main.domain.Item import Item
from main.domain.TradingSystemException import TradingSystemException

store_name1 = "TEST_store_roy"
item_name1 = "TEST_bamba"
store_name2 = "TEST_store_rotem"
item_name2 = "TEST_bisli"


class ItemStub(Item):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return 'item name'


# def setup_function(function):
#     facade = DomainFacade.DomainFacade()
#     session_id = facade.initiate_session()
#     facade.register(session_id, "TEST_store_owner", "123456")
#     facade.login(session_id, "TEST_store_owner", "123456")
#     facade.add_store(session_id, store_name1, "nice_store: writing enough words just to pass test", [])
#     facade.add_item_to_store(session_id, store_name1, item_name1, "category",
#                              "nice product", 12, 1)
#     facade.add_store(session_id, store_name2, "nice_store: writing enough words just to pass test", [])
#     facade.add_item_to_store(session_id, store_name1, item_name2, "category",
#                              "nice product", 16, 1)
#
#
# def teardown_function(function):
#     TradingSystem.TradingSystem.clear()


def test_register1():
    guest: Guest = Guest()
    assert guest.register("lala", "ererer") is True


def test_register2():
    guest: Guest = Guest()
    guest.register("lala", "ererer")
    assert guest.register("lala", "ererer") is False


def test_login1():
    guest: Guest = Guest()
    guest.register("lala", "ererer")
    assert guest.login("lala", "ererer") is True


def test_login2():
    guest: Guest = Guest()
    guest.register("lala", "ererer")
    assert guest.login("lala", "ereret") is False


def test_add_item_to_cart1():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    assert guest.has_item_in_cart(item.name, 'mock store')


def test_add_item_to_cart2():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    guest.add_item_to_cart(item, 'mock store')
    assert guest.check_quantity(item, 'mock store') == 2


def test_remove_item_from_cart1():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    guest.remove_item_from_cart(item, 'mock store')
    assert guest.check_quantity(item, 'mock store') == 0


# store doesn't exist
def test_remove_item_from_cart2():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    try:
        guest.remove_item_from_cart(item, 'mock store_oops')
        assert False
    except TradingSystemException as e:
        assert guest.check_quantity(item, 'mock store') == 1


# item doesnt exist
def test_remove_item_from_cart3():
    guest: Guest = Guest()
    item = ItemStub()
    item2 = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    try:
        guest.remove_item_from_cart(item2, 'mock store')
        assert False
    except TradingSystemException as e:
        assert guest.check_quantity(item, 'mock store') == 1


def test_change_item_quantity_in_cart1():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    guest.change_item_quantity_in_cart(item, 'mock store', 4)
    assert guest.check_quantity(item, 'mock store') == 5


# negative quantity
def test_change_item_quantity_in_cart2():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    try:
        guest.change_item_quantity_in_cart(item, 'mock store', -4)
        assert False
    except TradingSystemException as e:
        assert guest.check_quantity(item, 'mock store') == 1


# not existing store
def test_change_item_quantity_in_cart3():
    guest: Guest = Guest()
    item = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    try:
        guest.change_item_quantity_in_cart(item, 'mock store_oops', 2)
        assert False
    except TradingSystemException as e:
        assert guest.check_quantity(item, 'mock store') == 1


# not existing item
def test_change_item_quantity_in_cart4():
    guest: Guest = Guest()
    item = ItemStub()
    item2 = ItemStub()
    guest.add_item_to_cart(item, 'mock store')
    try:
        guest.change_item_quantity_in_cart(item2, 'mock store', 3)
        assert False
    except TradingSystemException as e:
        assert guest.check_quantity(item, 'mock store') == 1


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
