class CollectionSys(object):
    def __init__(self):
        pass

    _up = True

    @staticmethod
    def pay(creditcard, date, snum, price):
        return True

    @staticmethod
    def connect():
        return CollectionSys._up

    #for test
    def make_sys_fail(self):
        CollectionSys._up = False

    def make_sys_pass(self):
        CollectionSys._up = True
