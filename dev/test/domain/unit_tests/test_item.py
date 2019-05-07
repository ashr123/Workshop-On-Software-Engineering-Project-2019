from main.domain.Item import Item
from main.domain.TradingSystemException import TradingSystemException

def test_dec_quantity():
    item = Item(3, 'new product', 'excellent', 'Other', 4.2, 8)
    try:
        item.dec_quantity(9)
        assert False
    except TradingSystemException as e:
        assert True

def test_is_hashtag():
    item = Item(3, 'silver ring', 'sterling silver ring heart shaped with blue diamonds', 'Jewls', 4.2, 8)
    assert item.is_hashtaged('blue')
    assert item.is_hashtaged('jewls')
    assert item.is_hashtaged('ring')
    assert not item.is_hashtaged('dog')




