from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from tests.mainTest import MyUnitTesting
from trading_system import service


class TestTradingSystem(MyUnitTesting):
	def test_add_manager(self):
		store_pk = service.open_store("bla", "blabla", self.user.pk)
		User.objects.create(username="new_user", password=make_password(self.default_password))
		self.assertTrue(service.add_manager("new_user", [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False, store_pk, self.default_user)[0])
