from main.domain.TradingSystem import TradingSystem


def setup_module(module):
    pass


def teardown_module(module):
    pass

# integrate member and guest
def test_register():
    system = TradingSystem()
    id = system.generate_id()
    system.register_member(id, 'rotem', 'a8a8a8')
    user = system.get_user(id)
    member = system.get_member('rotem')
    assert member.get_guest == user


def test_register2():
    system = TradingSystem()
    system.clear()
    id = system.generate_id()
    system.register_member(id, 'rotem', 'a8a8a8')
    try:
        system.register_member(id, 'rotem', 'a8a8a8')
        assert False
    except Exception as e:
        assert e.msg == 'the user rotem is already registered'