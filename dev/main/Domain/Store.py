class Store(object):
    def __init__(self, items, name, creator, rules):
        self._items = items
        self._name = name
        self._creator = creator
        self._rules = rules
