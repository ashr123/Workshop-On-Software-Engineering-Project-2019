from main.Domain.User import User


class Member(User):

    def __init__(self, name):
        User.__init__(self)
        self._name = name
        self._storesManaged = []

    @property
    def name(self):
        return self._name

    def logout(self):
        return False

    def openStore(self):
        return False
