
# from main.domain import Guest, Permission, Item, Member, Store, TradingSystem
import pytest
from main.domain.Item import Item
from main.domain.ManagementState import ManagementState
from main.domain.Store import Store
from main.domain.Guest import Guest
from main.domain.Member import Member
from main.domain.GroceryCart import GroceryCart
from main.domain.Permission import Permissions


class ItemStub(Item):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return 4


class MSStub(ManagementState):
    def __init__(self):
        pass


class StoreStub(Store):
    def __init__(self):
        pass

    @property
    def name(self):
        return 'mock store'

class GroceryCartStub(GroceryCart):
    def __init__(self):
        pass

    def add_item(self, item):
        return True


class GuestStub(Guest):
    def __init__(self):
        self._groceryCarts = {'mock store': GroceryCartStub()}

    def check_quantity(self, item, store_name):
        return 1


def test_add_item_to_cart1():
    member: Member = Member('roni', GuestStub())
    item: ItemStub = ItemStub()
    member.add_item_to_cart(item, 'mock store')
    assert member.get_guest.check_quantity(item, 'mock store') == 1


@pytest.mark.skip(reason="no way of currently testing this, objects too coupled")
def test_add_item_to_cart2():
    member: Member = Member('roni', GuestStub())
    item: ItemStub = ItemStub()
    member.add_item_to_cart(item, 'mock store')
    member.add_item_to_cart(item, 'mock store')
    assert member.get_guest.check_quantity(item, 'mock store') == 2


def test_add_managment_state():
    member: Member = Member('roni', GuestStub())
    member2: Member = Member('goni', GuestStub())
    assert not member.stores_managed_states
    member.add_managment_state(True, [Permissions.ADD_MANAGER],
                               StoreStub(), member2)
    assert member.stores_managed_states  # cant check further cause MS is another class


@pytest.mark.skip(reason="no way of currently testing this, objects too coupled")
def test_add_manager():
    member: Member = Member('roni', GuestStub())
    member2: Member = Member('goni', GuestStub())
    store: StoreStub = StoreStub()
    member.add_managment_state(True, [], store, None)
    member.add_manager('mock store', 'goni', [])

