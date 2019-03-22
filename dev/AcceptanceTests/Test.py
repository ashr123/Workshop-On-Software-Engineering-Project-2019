from main.Service.Facade import Facade


def test_login():
    facade_instance = Facade()
    assert True == facade_instance.login("rotem", "123456")
