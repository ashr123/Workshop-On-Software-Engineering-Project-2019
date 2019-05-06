class SupplySys(object):
    def __init__(self):
        pass

    _up = True
    @staticmethod
    def supply(trans_id, address):
        return True

    @staticmethod
    def connect():
        return SupplySys._up


    #for test
    @staticmethod
    def make_sys_fail():
        SupplySys._up = False

    @staticmethod
    def make_sys_pass():
        SupplySys._up = True
