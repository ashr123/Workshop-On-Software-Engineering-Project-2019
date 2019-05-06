from main.external_systems.MoneyCollection import CollectionSys
from main.domain.TradingSystemException import MoneyCollectionException


class MoneyCollectionFacade(object):
    def __init__(self):
        self._sys = CollectionSys()

    def pay(self, creditcard, date, snum, price):
        if not self._sys.connect():
            raise MoneyCollectionException("collection system is down")
        if creditcard is None or date is None or snum is None or price is None:
            raise MoneyCollectionException("missing details to complete payment")
        return self._sys.pay(creditcard, date, snum, price)

    def connect(self):
        if not self._sys.connect():
            raise MoneyCollectionException("collection system is down")
        return True

    #for test
    def make_sys_fail(self):
        self._sys.make_sys_fail()

    def make_sys_pass(self):
        self._sys.make_sys_pass()
