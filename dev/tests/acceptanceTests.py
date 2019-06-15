import json
from unittest import skip, expectedFailure

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import DataError

from tests.mainTest import MyUnitTesting
from trading_system import service


class TestTradingSystem(MyUnitTesting):
	@skip("Not ready")
	def test_admin_register(self):  # 1.1-1
		pass

	@skip("Not ready")
	def test_admin_register_failed_username_or_password(self):  # 1.1-2
		pass

	@skip("Not ready")
	def test_admin_register_failed_money_collector(self):  # 1.1-3
		pass

	@skip("Not ready")
	def test_admin_register_failed_supply_system(self):  # 1.1-4
		pass

	@skip("Not ready")
	def test_admin_register_failed_supply_system(self):  # 1.1-5
		pass

	@skip("Not ready")
	def test_guest_register_none_existing_user(self):  # 2.2-1
		pass

	@skip("Not ready")
	def test_guest_register_with_existing_user(self):  # 2.2-2
		pass

	@skip("Not ready")
	def test_guest_register_none_existing_user_illegal_password(self):  # 2.2-3
		pass

	@skip("Not ready")
	def test_guest_login_with_existing_user(self):  # 2.3-1
		pass

	@skip("Not ready")
	def test_guest_login_none_existing_user(self):  # 2.3-2
		pass

	@skip("Not ready")
	def test_guest_login_with_existing_user_illegal_password(self):  # 2.3-3
		pass

	@skip("Not ready")
	def test_member_login(self):  # 2.3-4
		pass

	def test_search_by_name_fur_shampoo_exists(self):  # 2.5-1
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": "fur shampoo",
		                                      "description": "This is a fur shampoo",
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.assertTrue(list(service.search("fur shampoo")))

	@skip("Not relevant")
	def test_search_with_empty_field(self):  # 2.5-2
		pass

	def test_search_none_existing_item(self):  # 2.5-3...
		self.assertFalse(list(service.search("A none relevant item")))

	@skip("Not ready: missing function related to cart in service")
	def test_member_adds_to_empty_cart_an_existing_product(self):  # 2.6-1...
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": "fur shampoo 2",
		                                      "description": "This is a fur shampoo 2",
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.login(self.default_user, self.default_password)

	@skip("Not ready: can't buy item at all")
	def test_buy_existing_item(self):  # 2.8.1-1
		pass

	@skip("Not ready: can't buy item at all")
	def test_buy_existing_item_x2_but_only_exists_1_in_inventory(self):  # 2.8.1-2...
		pass

	@skip("Can't check if user is logged in (probably only through request")
	def test_member_logout(self):  # 3.1-1...
		res = self.user.is_authenticated
		res = User.objects.get(username=self.default_user).is_authenticated
		self.driver.get(self.live_server_url + "/accounts/logout/")
		res = self.user.is_authenticated
		res = User.objects.get(username=self.default_user).is_authenticated
		self.login(self.default_user, self.default_password)
		res = self.user.is_authenticated
		res = User.objects.get(username=self.default_user).is_authenticated
		self.driver.get(self.live_server_url + "/accounts/logout/")
		res = self.user.is_authenticated
		res = User.objects.get(username=self.default_user).is_authenticated
		self.assertTrue(True)

	def test_store_owner_adds_item_to_store(self):  # 4.1.1-1
		self.assertTrue(self.user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 3"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.assertTrue(self.store.items.filter(name=item_name).exists())

	def test_not_store_owner_adds_item_to_store(self):  # 4.1.1-2
		user = User.objects.create(username="temp_user", password=make_password(self.default_password))
		self.assertFalse(user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 4"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.assertFalse(self.store.items.filter(name=item_name).exists())

	@skip("Not relevant")
	def test_store_owner_adds_already_existing_item_to_store(self):  # 4.1.1
		self.assertTrue(self.user.groups.filter(name='store_owners').exists())
		item_name: str = "fur shampoo 5"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.assertTrue(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)

	def test_adding_item_with_negative_quantity(self):  # 4.1.1-5
		self.assertTrue(self.user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 6"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		with self.assertRaises(DataError):
			service.add_item_to_store(json.dumps({"price": 12.34,
			                                      "name": item_name,
			                                      "description": "This is a %s" % item_name,
			                                      "category": "HOME",
			                                      "quantity": -12}), self.store.pk)
		self.assertFalse(self.store.items.filter(name=item_name).exists())

	@expectedFailure
	def test_adding_item_with_float_quantity(self):  # 4.1.1-6
		self.assertTrue(self.user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 7"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		# with self.assertRaises(DataError):
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 0.3}), self.store.pk)

		self.assertFalse(self.store.items.filter(name=item_name).exists())

	@skip("there isn't a function for deletion yet")
	def test_delete_an_item_from_store(self):  # 4.1.2-1...
		user = User.objects.create(username="temp_user", password=make_password(self.default_password))
		self.assertFalse(user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 4"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk)
		self.assertFalse(self.store.items.filter(name=item_name).exists())

	@skip("there isn't a function for deletion yet")
	def test_edit_an_existing_item(self):  # 4.1.3-1...
		pass

	def test_add_owner_to_store(self):  # 4.3-1
		new_user = User.objects.create(username="new_user", password=make_password(self.default_password))
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.default_user)[0])
		self.assertTrue(service.get_user_store_list(new_user.pk))

	def test_add_owner_to_store_by_none_owner(self):  # 4.3-2
		new_user = User.objects.create(username="new_user2", password=make_password(self.default_password))
		new_user2 = User.objects.create(username="new_user3", password=make_password(self.default_password))
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertTrue(service.add_manager(new_user.username, [], True, self.store.pk, new_user2.username)[0])
		self.assertFalse(service.get_user_store_list(new_user.pk))

	def test_add_guest_to_store_by_store_owner(self):  # 4.3-3
		self.assertTrue(service.add_manager("Moshe", [], True, self.store.pk, self.default_user)[0])

	def test_make_reflexive_ownership(self):  # 4.3-2
		new_user = User.objects.create(username="new_user4", password=make_password(self.default_password))
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.user.username)[0])
		self.assertTrue(service.get_user_store_list(new_user.pk))
		self.assertTrue(service.add_manager(self.user.username, [], True, self.store.pk, new_user.username)[0])

	def test_delete_owner_by_another_owner(self):  # 4.4-1
		new_user = User.objects.create(username="new_user5", password=make_password(self.default_password))
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.user.username)[0])
		


	def test_add_manager(self):
		store_pk = service.open_store("bla", "blabla", self.user.pk)
		User.objects.create(username="new_user", password=make_password(self.default_password))
		self.assertFalse(
			service.add_manager("new_user", [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False, store_pk,
			                    self.default_user)[0])
