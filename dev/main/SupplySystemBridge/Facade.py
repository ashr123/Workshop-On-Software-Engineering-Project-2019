from main.external_systems.Supply import SupplySys
from main.domain.TradingSystemException import SupplyException


class SupplyFacade(object):
    def __init__(self):
        self._sys = SupplySys()

    def supply(self, trans_id, address):
        if not self._sys.connect():
            raise SupplyException("supply system is down")
        return self._sys.supply(trans_id, address)

    def connect(self):
        if not self._sys.connect():
            raise SupplyException("supply system is down")
        return True

    #for test
    def make_sys_fail(self):
        self._sys.make_sys_fail()

    def make_sys_pass(self):
        self._sys.make_sys_pass()