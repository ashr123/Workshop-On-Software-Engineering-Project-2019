from main.domain.Purchase import Purchase

# check functionality when items list is empty
def test_add_item_and_amount1():
    purchase = Purchase(1, 4)
    assert len(purchase.items) == 0
    purchase.add_item_and_amount('store1', 'item1', 4)
    assert len(purchase.items) == 1
    assert purchase.items[0]['store'] == 'store1'
    assert len(purchase.items[0]['items']) == 1
    assert purchase.items[0]['items'][0]['item_name'] == 'item1'
    assert purchase.items[0]['items'][0]['amount'] == 4

# check functionality when items list not empty but lacks specific store
def test_add_item_and_amount2():
    purchase = Purchase(1, 4)
    purchase.add_item_and_amount('store1', 'item1', 4)
    purchase.add_item_and_amount('store2', 'item2', 44)
    assert len(purchase.items) == 2
    assert purchase.items[1]['store'] == 'store2'
    assert len(purchase.items[1]['items']) == 1
    assert purchase.items[1]['items'][0]['item_name'] == 'item2'
    assert purchase.items[1]['items'][0]['amount'] == 44


# check functionality when adding another item of the same store
def test_add_item_and_amount3():
    purchase = Purchase(1, 4)
    purchase.add_item_and_amount('store1', 'item1', 4)
    purchase.add_item_and_amount('store1', 'item2', 44)
    assert len(purchase.items) == 1
    assert purchase.items[0]['store'] == 'store1'
    assert len(purchase.items[0]['items']) == 2
    assert purchase.items[0]['items'][1]['item_name'] == 'item2'
    assert purchase.items[0]['items'][1]['amount'] == 44
