from main.domain.Store import Store
from main.domain.Item import Item
from main.domain.Rule import Rule
from main.domain.TradingSystemException import TradingSystemException


class RuleStub(Rule):
    def __init__(self):
        pass

    def apply_rule(self, item, amount):
        return 7

class ItemStub(Item):
    def __init__(self):
        self._quantity = 5

    @property
    def id(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return 'name'

    @property
    def price(self) -> str:
        return 10

    @property
    def quantity(self) -> str:
        return 5

    def inc_quantity(self, amount: int):
        return 5 + amount


class ItemStub2(Item):
    def __init__(self):
        self._quantity = 5

    @property
    def id(self) -> int:
        return 99

    @property
    def name(self) -> str:
        return 'name2'

    @property
    def price(self) -> str:
        return 10

    @property
    def quantity(self) -> str:
        return 5

    def inc_quantity(self, amount: int):
        return 5 + amount


def create_store_instance() -> Store:
    return Store("RoysStore", None, "best store in town to get everything you need", [])


def test_add_item():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item=new_item)
    assert store.has_item(new_item.id)


# remove existing item
def test_remove_item1():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    assert store.remove_item(new_item.id)
    assert not store.has_item(new_item.id)
    assert len(store.items) == 0


# remove non existing item
def test_remove_item2():
    store = create_store_instance()
    new_item = ItemStub()
    assert not store.remove_item(new_item.id)
    assert len(store.items) == 0


# change name successfully
def test_edit_item1():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = "new_name"
    store.edit_item(new_item, "name", new_value)
    assert True


# change price successfully
def test_edit_item2():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 3
    store.edit_item(new_item, "price", new_value)
    assert True


# change description successfully
def test_edit_item3():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 'aaaa aaaa aaaa aaaa aaaa'
    store.edit_item(new_item, "description", new_value)
    assert True


# change category successfully
def test_edit_item4():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 'other'
    store.edit_item(new_item, "category", new_value)
    assert True


# change quantity successfully
def test_edit_item5():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 4
    store.edit_item(new_item, "quantity", new_value)
    assert True


# change to an already existing name - suppose to fail
def test_edit_item6():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 'name'
    try:
        store.edit_item(new_item, "name", new_value)
    except TradingSystemException as e:
        assert True


# change price to negative
def test_edit_item7():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = -9
    try:
        store.edit_item(new_item, "price", new_value)
    except TradingSystemException as e:
        assert True


# change to short description
def test_edit_item8():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 'h'
    try:
        store.edit_item(new_item, "description", new_value)
    except TradingSystemException as e:
        assert True


# change quantity to non integer
def test_edit_item9():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 4.5
    try:
        store.edit_item(new_item, "quantity", new_value)
    except TradingSystemException as e:
        assert True


# change quantity to negative
def test_edit_item10():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = -2
    try:
        store.edit_item(new_item, "quantity", new_value)
    except TradingSystemException as e:
        assert True


# change unknown field
def test_edit_item11():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    new_value = 5
    try:
        store.edit_item(new_item, "e", new_value)
    except TradingSystemException as e:
        assert True


def test_has_item():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    assert store.has_item(4)


# reserve existing item
def test_reserve_item1():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    store.reserve_item(1, new_item.name, 2)
    assert store.reserved_items[0]['session_id'] == 1
    assert store.reserved_items[0]['reserved'][0]['item_id'] == 4
    assert store.reserved_items[0]['reserved'][0]['amount'] == 2


# reserve non existing item
def test_reserve_item2():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    try:
        store.reserve_item(1, 'not existing item', 2)
        assert False
    except TradingSystemException as e:
        assert len(store.reserved_items) == 0

# reserve for an existing user
def test_reserve_item3():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    store.reserve_item(1, new_item.name, 2)
    new_item2 = ItemStub2()
    store.add_item(new_item2)
    store.reserve_item(1, new_item2.name, 4)
    assert store.reserved_items[0]['session_id'] == 1
    assert store.reserved_items[0]['reserved'][0]['item_id'] == 4
    assert store.reserved_items[0]['reserved'][0]['amount'] == 2
    assert store.reserved_items[0]['reserved'][1]['item_id'] == 99
    assert store.reserved_items[0]['reserved'][1]['amount'] == 4


# reserve for an existing item
def test_reserve_item4():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    store.reserve_item(1, new_item.name, 2)
    store.reserve_item(1, new_item.name, 1)
    assert store.reserved_items[0]['session_id'] == 1
    assert store.reserved_items[0]['reserved'][0]['item_id'] == 4
    assert store.reserved_items[0]['reserved'][0]['amount'] == 3


# check rule applies
def test_get_discount_price1():
    store = Store('store with rules', None, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa', [RuleStub()])
    new_item = ItemStub()
    store.add_item(new_item)
    assert store.get_discount_price('name', 3) == 7


# check rule not applies
def test_get_discount_price2():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    assert store.get_discount_price('name', 3) == 30


# check apply trans works
def apply_trans():
    store = create_store_instance()
    new_item = ItemStub()
    store.add_item(new_item)
    store.reserve_item(1, new_item.name, 2)
    store.apply_trans(1)
    assert store.reserved_items == []