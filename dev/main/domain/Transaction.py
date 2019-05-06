from functools import reduce


class Transaction(object):
    def __init__(self, id, session_id, store_name):
        self._id = id
        self._session_id = session_id
        self._store_name = store_name
        self._items = []
        self._is_supply_approved = False
        self._is_payment_approved = False

    @property
    def id(self):
        return self._id

    @property
    def store_name(self):
        return self._store_name

    @property
    def is_supply_approved(self):
        return self._is_supply_approved

    @property
    def is_payment_approved(self):
        return self._is_payment_approved

    @property
    def items(self):
        return self._items

    @property
    def store_name(self):
        return self._store_name

    def add_item_and_amount(self, item_name, amount):
        return self._items.append({"item_name": item_name, "amount": amount})

    def pay_succ(self):
        self._is_payment_approved = True

    def supply_succ(self):
        self._is_supply_approved = True