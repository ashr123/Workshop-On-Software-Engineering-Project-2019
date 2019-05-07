from main.domain.Item import Item
from main.domain.TradingSystem import TradingSystem


class ItemStub(Item):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return 4

    @property
    def name(self) -> int:
        return 'im going mad'


# integrate member store and managmentState
def test_open_store():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    system.register_member(id, 'rotem', '090909')
    system.login(id, 'rotem', '090909')
    system.open_store(id, 'mock store', 'kgkgkgkggkgkgkgkgkgkgkgkgkg', [])
    assert system.get_store('mock store').description == 'kgkgkgkggkgkgkgkgkgkgkgkgkg'


def test_open_store2():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    try:
        system.open_store(id, 'mock store', 'kgkgkgkggkgkgkgkgkgkgkgkgkg', [])
        assert False
    except Exception as e:
        assert e.msg == 'you are not a member!'


def test_open_store3():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    system.register_member(id, 'rotem', '090909')
    system.login(id, 'rotem', '090909')
    system.open_store(id, 'mock store', 'kgkgkgkggkgkgkgkgkgkgkgkgkg', [])
    try:
        system.open_store(id, 'mock store', 'kgkgkgkggkgkgkgkgkgkgkgkgkg', [])
        assert False
    except Exception as e:
        assert e.msg == 'store mock store already exists'


def test_open_store4():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    system.register_member(id, 'rotem', '090909')
    system.login(id, 'rotem', '090909')
    try:
        system.open_store(id, 'mock store', 'kg', [])
        assert False
    except Exception as e:
        assert e.msg == 'description is too short'


def test_add_item_to_cart():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    system.get_user(id).add_item_to_cart(item, 'mock store')
    assert system.get_user(id).has_item_in_cart('im going mad', 'mock store')


def test_remove_item_from_cart():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    system.get_user(id).add_item_to_cart(item, 'mock store')
    system.get_user(id).remove_item_from_cart(item, 'mock store')
    assert not system.get_user(id).has_item_in_cart('im going mad', 'mock store')

def test_edit_item_in_cart():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    system.get_user(id).add_item_to_cart(item, 'mock store')
    system.get_user(id).change_item_quantity_in_cart(item, 'mock store', -1)
    assert system.get_user(id).check_quantity(item, 'mock store') == 0

def test_edit_item_in_cart2():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    system.get_user(id).add_item_to_cart(item, 'mock store')
    try:
        system.get_user(id).change_item_quantity_in_cart(item, 'mock store', -4)
        assert False
    except Exception as e:
        assert system.get_user(id).check_quantity(item, 'mock store') == 1
