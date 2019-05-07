from main.domain.GroceryCart import GroceryCart
from main.domain.Item import Item
from main.domain.TradingSystemException import TradingSystemException

class ItemStub(Item):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return 4

# adding new item
def test_add_item1():
    grocery = GroceryCart('test store')
    assert len(grocery.items) == 0
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    assert len(grocery.items) == 1
    assert grocery.items[item] == 1

# adding more of existing item
def test_add_item2():
    grocery = GroceryCart('test store')
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    grocery.add_item(item)
    assert len(grocery.items) == 1
    assert grocery.items[item] == 2

# adding new item to an existing grocery
def test_add_item3():
    grocery = GroceryCart('test store')
    item1: ItemStub = ItemStub()
    item2: ItemStub = ItemStub()
    grocery.add_item(item1)
    grocery.add_item(item2)
    assert len(grocery.items) == 2
    assert grocery.items[item1] == 1
    assert grocery.items[item2] == 1

# remove existing item
def test_remove_item1():
    grocery = GroceryCart('test store')
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    grocery.remove_item(item)
    assert len(grocery.items) == 0
    assert not grocery.has_item(4)


# remove non-existing item
def test_remove_item2():
    grocery = GroceryCart('test store')
    item: ItemStub = ItemStub()
    try:
        grocery.remove_item(item)
        assert False
    except TradingSystemException as e:
        assert True

# check positive change
def test_change_item_quantity_in_cart1():
    grocery: GroceryCart = GroceryCart('test store')
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    grocery.change_item_quantity_in_cart(item, 5)
    assert grocery.items[item] == 6

# check good negative change
def test_change_item_quantity_in_cart2():
    grocery: GroceryCart = GroceryCart('test store')
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    grocery.change_item_quantity_in_cart(item, -1)
    assert grocery.items[item] == 0

# check not good negative change
def test_change_item_quantity_in_cart3():
    grocery: GroceryCart = GroceryCart('test store')
    item: ItemStub = ItemStub()
    grocery.add_item(item)
    try:
        grocery.change_item_quantity_in_cart(item, -2)
        assert False
    except TradingSystemException as e:
        assert grocery.items[item] == 1

# non existing item
def test_change_item_quantity_in_cart4():
    grocery: GroceryCart = GroceryCart('test store')
    item: ItemStub = ItemStub()
    try:
        grocery.change_item_quantity_in_cart(item, 5)
        assert False
    except TradingSystemException as e:
        assert len(grocery.items) == 0
