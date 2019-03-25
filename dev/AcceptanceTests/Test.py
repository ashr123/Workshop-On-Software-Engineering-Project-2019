from main.Service.Facade import Facade


def test_setup():
	assert False


def test_login():
	facade_instance: Facade = Facade()
	assert True == facade_instance.login("rotem", "123456")
