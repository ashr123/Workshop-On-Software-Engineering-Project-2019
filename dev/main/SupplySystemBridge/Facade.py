from main.external_systems.Supply import SupplySys
from main.domain.TradingSystemException import SupplyException


class SupplyFacade(object):
    def __init__(self):
        self._sys = SupplySys()

    def supply(self, trans_id, package_details,  address):
        if not self._sys.connect():
            raise SupplyException("supply system is down")
        if trans_id is None or address is None:
            raise SupplyException("missing details to complete supply")
        return self._sys.supply(trans_id, package_details, address)

    def connect(self):
        if not self._sys.connect():
            raise SupplyException("supply system is down")
        return True

    #for test
    def make_sys_fail(self):
        self._sys.make_sys_fail()

    def make_sys_pass(self):
        self._sys.make_sys_pass()