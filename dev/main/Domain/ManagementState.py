class StoreManager(object):

    def __init__(self, isOwner, permissions):
        self._isOwner = isOwner
        self._permissions = permissions

    @property
    def isOwner(self):
        return self._isOwner

    @property
    def permissions(self):
        return self._permissions

    def addItem(self):
        return False

    def removeItem(self, itemId):
        return False

    def editItem(self, itemId):
        return False

    def addOwner(self, memberId):
        return False

    def removeOwner(self, memberId):
        return False

    def addManager(self, managerId):
        return False

    def removeManager(self, managerId):
        return False

    def setManagerPermissions(self, managerId):
        return False
