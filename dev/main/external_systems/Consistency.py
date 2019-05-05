class ConsistencySys(object):
    def __init__(self):
        pass
    _up = True

    @staticmethod
    def is_valid():
        return True

    @staticmethod
    def connect():
        return ConsistencySys._up

    #for test
    def make_sys_fail(self):
        ConsistencySys._up = False

    def make_sys_pass(self):
        ConsistencySys._up = True