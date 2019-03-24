class Item(object):
    def __init__(self, id, name, price):
        self._id = id
        self._name = name
        self._price = price

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price
