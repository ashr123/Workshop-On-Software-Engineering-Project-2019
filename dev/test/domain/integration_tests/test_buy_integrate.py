from main.domain.Item import Item
from main.domain.Store import Store
from main.domain.Purchase import Purchase
from main.domain.TradingSystem import TradingSystem
from main.CollectionSystemBridge.Facade import MoneyCollectionFacade
from main.SupplySystemBridge.Facade import SupplyFacade

class ItemStub(Item):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return 4

    @property
    def name(self) -> int:
        return 'im going mad'


    @property
    def price(self) -> int:
        return 34


class StoreStub(Store):
    def __init__(self):
        self._rules = []

    @property
    def name(self):
        return 'mock'

    def reserve_item(self, session_id: int, item_name: str, amount: int):
        return True


    def reserve_item2(self, session_id: int, item_name: str, amount: int):
        return False

    def get_item_by_name(self, item_name):
        return ItemStub()

    def apply_trans(self, session_id):
        return True

class StoreStub2(StoreStub):
    def __init__(self):
        self._rules = []

    @property
    def name(self):
        return 'mock2'


# integrate member transction
def test_buy():
   try:
        system = TradingSystem()
        system.clear()
        id = system.generate_id()
        trans = system.createTransaction(id, 'mock')
        assert trans == 1
        item = ItemStub()
        system.add_item_to_trans(trans, item.name, 9)
        transo = system.get_trans(trans)
        assert transo.items == [{'item_name': 'im going mad', 'amount': 9}]
        # cant check order now, belongs to store
       #  system.check_order(transo, 'rishon le zion')
       # assert system.calculate_price(transo) == 306
       # system.apply_trans(id, trans)
        #assert transo.items == []
   except Exception as e:
       assert False


# integrate member transction - add calls to external systems bridges - not involving store!
def test_buy1():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    try:
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 32)
        trans = system.get_trans(trans_id)
        # cant check order now, belongs to store
       # system.check_order(trans, 'rishon le zion')
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
       # price = system.calculate_price(trans)
        if MoneyCollectionFacade().pay('1212', '4/4', '555', 85):
            trans.pay_succ()
#            system.apply_trans(id, trans_id)
        assert system.get_trans(trans_id).items == [{'amount': 32, 'item_name': 'im going mad'}]
    except Exception as e:
        assert False

# sabotage collection system
def test_buy2():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    try:
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 32)
        trans = system.get_trans(trans_id)
       # system.check_order(trans, None)
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
      #  price = system.calculate_price(trans)
        if MoneyCollectionFacade().pay('1212', '4/4', '555', 85):
            trans.pay_succ()
            system.apply_trans(id, trans_id)
        assert system.get_trans(trans_id).items == []
        assert False
    except Exception as e:
        assert True


# sabotage supply system
def test_buy3():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    try:
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 32)
        trans = system.get_trans(trans_id)
        # system.check_order(trans, 'Rishon Le Zion')
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
       # price = system.calculate_price(trans)
        if MoneyCollectionFacade().pay('1212', None, '555', 43):
            trans.pay_succ()
            system.apply_trans(id, trans_id)
        assert system.get_trans(trans_id).items == []
        assert False
    except Exception as e:
        assert True


# now involve store
def test_buy4():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    store = StoreStub()
    system.t_add_to_stores(store)
    try:
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 32)
        trans = system.get_trans(trans_id)
        system.check_order(trans, 'Rishon Le Zion')
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
        price = system.calculate_price(trans)
        bol = MoneyCollectionFacade().pay('1212', '1212', '555', price)
        if bol:
            trans.pay_succ()
            assert system.apply_trans(id, trans_id)
        elif not bol:
            assert False
    except Exception as e:
        assert False

def test_buy5():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    store = StoreStub()
    system.t_add_to_stores(store)
    try:
        store.reserve_item(session_id=id, item_name=item.name, amount=4)
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 4)
        trans = system.get_trans(trans_id)
        system.check_order(trans, 'rishon le zion')
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
        price = system.calculate_price(trans)
        bol = MoneyCollectionFacade().pay('1212', '4/4', '555', price)
        if bol:
            trans.pay_succ()
            assert system.apply_trans(id, trans_id)
        elif not bol:
            assert False
    except Exception as e:
        assert False


def test_buy6():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    store = StoreStub()
    try:
        store.reserve_item2(session_id=id, item_name=item.name, amount=4)
        trans_id = system.createTransaction(id, 'mock')
        system.add_item_to_trans(trans_id, item.name, 4)
        trans = system.get_trans(trans_id)
        system.check_order(trans, 'rishon le zion')
        if SupplyFacade().supply(trans_id, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
        price = system.calculate_price(trans)
        if MoneyCollectionFacade().pay('1212', '4/4', '555', price):
            trans.pay_succ()
            system.apply_trans(id, trans_id)
        assert system.get_trans(trans_id).items == []
        assert False
    except Exception as e:
        assert True

# from cart
def test_buy7():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    item = ItemStub()
    store = StoreStub()
    system.t_add_to_stores(store)
    item2 = ItemStub()
    store2 = StoreStub2()
    system.t_add_to_stores(store2)
    try:
        purchase = TradingSystem.createPurchase(id)
        store.reserve_item(session_id=id, item_name=item.name, amount=4)
        store2.reserve_item(session_id=id, item_name=item2.name, amount=4)
        system.add_item_to_purch(purchase, store.name, item.name, 4)
        system.add_item_to_purch(purchase, store2.name, item2.name, 4)
        trans = system.get_trans(purchase)
        system.check_order(trans, 'rishon le zion')
        if SupplyFacade().supply(purchase, trans.num_of_items, 'rishon le zion'):
            trans.supply_succ()
        price = system.calculate_price(trans)
        bol = MoneyCollectionFacade().pay('1212', '4/4', '555', price)
        if bol:
            trans.pay_succ()
            assert trans.num_of_items == 8
        elif not bol:
            assert False
    except Exception as e:
        assert False