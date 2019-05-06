from main.domain.Rule import Rule


class Purchase(Rule):
    def __init__(self, id, session_id):
        self._id = id
        self._session_id = session_id
        self._items = []  # [{store, [{item, amount}]}]
        self._is_supply_approved = False
        self._is_payment_approved = False
        self._num_of_items = 0
        self._is_purchase = True

    @property
    def id(self):
        return self._id

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
    def num_of_items(self):
        return self._num_of_items

    def add_item_and_amount(self, store_name, item_name, amount):
        list_of_items = list(filter(lambda i: i["store"] == store_name, self.items))
        if len(list_of_items) == 0:
            self.items.append({"store": store_name, "items": []})
            list_of_items = [self.items[-1]]
        (list_of_items[0]["items"]).append({"item_name": item_name, "amount": amount})
        self._num_of_items += amount

    def pay_succ(self):
        self._is_payment_approved = True

    def supply_succ(self):
        self._is_supply_approved = True




