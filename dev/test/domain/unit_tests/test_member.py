from main.domain.Guest import Guest
from main.domain.Member import Member
from main.domain.Item import Item
from main.domain.ManagementState import ManagementState
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


class StoreStub(Guest):
    def __init__(self):
        pass


class GuestStub(Guest):
    def __init__(self):
        pass

    # def check_quantity(self, item, store_name):
    #     return 1


def test_add_item_to_cart1():
    member: Member = Member('roni', GuestStub())
    item: ItemStub = ItemStub()
    member.add_item_to_cart(item, 'mock store')
    assert member.get_guest.check_quantity(item, 'mock store') == 1

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


def test_add_manager():
    member: Member.Member = Member.Member("Roy", Guest.Guest())
    member2: Member.Member = Member.Member("Rotem", Guest.Guest())
    member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
                               Store.Store("Second store", member, "bla bla bla"), member2)
    TradingSystem.TradingSystem.add_member(member2)
    member.add_manager("Second store", "Rotem", [Permission.Permissions.ADD_MANAGER])
    TradingSystem.TradingSystem.clear()
    assert True


# def test_remove_owner():
#     member: Member.Member = Member.Member("Roy", Guest.Guest())
#     member2: Member.Member = Member.Member("Rotem", Guest.Guest())
#     store: Store.Store = Store.Store("Second store", member2, "bla bla bla")
#     member.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
#                                store, member2)
#     member2.add_managment_state(True, [Permission.Permissions.ADD_MANAGER],
#                                 store, member)
#     store.add_owner(member)
#     TradingSystem.TradingSystem.add_member(member)
#     TradingSystem.TradingSystem.add_member(member2)
#     member2.remove_owner("Second store", "Roy")
#     TradingSystem.TradingSystem.clear()
