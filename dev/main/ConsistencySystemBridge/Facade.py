from main.external_systems.Consistency import ConsistencySys
from main.domain.TradingSystemException import ConsistencyException


class ConsistencyFacade(object):
    def __init__(self):
        self._sys = ConsistencySys()

    def is_valid(self, rules):
        return self._sys.is_valid(rules)

    def connect(self):
        if not self._sys.connect():
            raise ConsistencyException("consistency system is down")
        return True

    #for test
    def make_sys_fail(self):
        self._sys.make_sys_fail()

    def make_sys_pass(self):
        self._sys.make_sys_pass()

