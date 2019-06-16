import json
from unittest import skip, expectedFailure

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import DataError

from store.models import Store
from tests.mainTest import MyUnitTesting
from trading_system import service


def user_with_default_password_generator():
	user_num = 0
	while True:
		yield User.objects.create(username="new_user%d" % user_num,
		                          password=make_password(MyUnitTesting.default_password))
		user_num += 1


def store_generator():
	store_num = 0
	while True:
		user_pk = yield
		yield service.open_store("bla%d" % store_num, "blabla", user_pk)
		store_num += 1


class TestTradingSystem(MyUnitTesting):
	generate_user_with_default_password = user_with_default_password_generator()
	generate_store1 = store_generator()

	@classmethod
	def generate_store(cls, user):
		next(cls.generate_store1)
		return cls.generate_store1.send(user.pk)

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
		                                      "quantity": 12}), self.store.pk, self.user.pk)
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
		                                      "quantity": 12}), self.store.pk, self.user.pk)
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
		output = service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk, self.user.pk)
		self.assertTrue(self.store.items.filter(name=item_name).exists())

	def test_not_store_owner_adds_item_to_store(self):  # 4.1.1-2
		user = next(self.generate_user_with_default_password)
		self.assertFalse(user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 4"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk, user.pk)
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
		                                      "quantity": 12}), self.store.pk, self.user.pk)
		self.assertTrue(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk, self.user.pk)

	def test_adding_item_with_negative_quantity(self):  # 4.1.1-5
		self.assertTrue(self.user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 6"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		with self.assertRaises(DataError):
			service.add_item_to_store(json.dumps({"price": 12.34,
			                                      "name": item_name,
			                                      "description": "This is a %s" % item_name,
			                                      "category": "HOME",
			                                      "quantity": -12}), self.store.pk, self.user.pk)
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
		                                      "quantity": 0.3}), self.store.pk, self.user.pk)

		self.assertFalse(self.store.items.filter(name=item_name).exists())

	def test_delete_an_item_from_store(self):  # 4.1.2-1... TODO: complete
		user = next(self.generate_user_with_default_password)
		self.assertFalse(user.groups.filter(name='store_owners').exists())
		item_name = "fur shampoo 4"
		self.assertFalse(self.store.items.filter(name=item_name).exists())
		service.add_item_to_store(json.dumps({"price": 12.34,
		                                      "name": item_name,
		                                      "description": "This is a %s" % item_name,
		                                      "category": "HOME",
		                                      "quantity": 12}), self.store.pk, self.user.pk)
		self.assertFalse(self.store.items.filter(name=item_name).exists())

	@skip("there isn't a function for deletion yet")
	def test_edit_an_existing_item(self):  # 4.1.3-1...
		pass

	def test_add_owner_to_store(self):  # 4.3-1
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.default_user)[0])
		self.assertTrue(service.get_user_store_list(new_user.pk))

	def test_add_owner_to_store_by_none_owner(self):  # 4.3-2
		new_user = next(self.generate_user_with_default_password)
		new_user2 = next(self.generate_user_with_default_password)
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertTrue(service.add_manager(new_user.username, [], True, self.store.pk, new_user2.username)[0])
		self.assertFalse(service.get_user_store_list(new_user.pk))

	def test_add_guest_to_store_by_store_owner(self):  # 4.3-3
		self.assertTrue(service.add_manager("Moshe", [], True, self.store.pk, self.default_user)[0])

	def test_make_reflexive_ownership(self):  # 4.3-2
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.user.username)[0])
		self.assertTrue(service.get_user_store_list(new_user.pk))
		self.assertTrue(service.add_manager(self.user.username, [], True, self.store.pk, new_user.username)[0])

	def test_delete_owner_by_another_owner(self):  # 4.4-1
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(service.add_manager(new_user.username, [], True, self.store.pk, self.user.username)[0])
		self.assertTrue(service.remove_manager_from_store(self.store.pk, new_user.pk))

	@skip("chain of ownership doesn't implemented")
	def test_delete_first_owner_by_second_owner_that_didnt_ownered_the_first_owner(self):  # 4.4-2
		pass

	@skip("permission for deleting from store doesn't exist")
	def test_delete_an_owner_by_none_owner(self):  # 4.4-3
		new_user = next(self.generate_user_with_default_password)
		new_user2 = next(self.generate_user_with_default_password)
		self.assertFalse(service.get_user_store_list(new_user.pk))
		self.assertTrue(service.add_manager(new_user.username, [], True, self.store.pk, self.user.username)[0])
		self.assertFalse(service.remove_manager_from_store(self.store.pk, new_user.pk))
		self.assertFalse(service.get_user_store_list(new_user.pk))

	@skip("permission for deleting from store doesn't exist, not ready")
	def test_delete_a_none_owner_by_owner(self):  # 4.4-4
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(service.get_user_store_list(new_user.pk))

	def test_add_manager_with_edit_permission(self):  # 4.5-1
		store_pk = self.generate_store(self.user)
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(
			service.add_manager(new_user.username, [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False,
			                    store_pk,
			                    self.default_user)[0])
		self.assertTrue(new_user.has_perm(self.Perms.EDIT_ITEM.value, Store.objects.get(pk=store_pk)))

	def test_add_manager_by_none_owner(self):  # 4.5-2
		store_pk = self.generate_store(self.user)
		new_user = next(self.generate_user_with_default_password)
		new_user2 = next(self.generate_user_with_default_password)
		self.assertTrue(
			service.add_manager(new_user.username, [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False,
			                    store_pk,
			                    new_user2.username)[0])
		self.assertFalse(new_user.has_perm(self.Perms.EDIT_ITEM.value, Store.objects.get(pk=store_pk)))

	def test_add_manager_that_already_manages_the_store(self):  # 4.5-3
		store_pk = self.generate_store(self.user)
		new_user = next(self.generate_user_with_default_password)
		self.assertFalse(
			service.add_manager(new_user.username, [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False,
			                    store_pk,
			                    self.default_user)[0])
		self.assertTrue(new_user.has_perm(self.Perms.EDIT_ITEM.value, Store.objects.get(pk=store_pk)))
		self.assertTrue(
			service.add_manager(new_user.username, [self.Perms.ADD_ITEM.value, self.Perms.EDIT_ITEM.value], False,
			                    store_pk,
			                    self.default_user)[0])

	@skip("permission checking doesn't exist")
	def test_remove_manager(self):  # 4.6-1
		pass

	def test_delete_existing_item_from_store(self):  # 5.1-1
		item_name = "bbb"
		item_dict = {"price": 12.34,
		             "name": item_name,
		             "description": "This is a %s" % item_name,
		             "category": "HOME",
		             "quantity": 12}
		service.add_item_to_store(json.dumps(item_dict), self.store.pk, self.user.pk)
		self.assertTrue(item_dict["name"] == service.get_store_items(self.store.pk)[0]["name"])
		service.delete_item(service.get_store_items(self.store.pk)[0]["id"], self.user.pk)
		self.assertFalse(service.get_store_items(self.store.pk))

	@skip("need to fix 'delete_item' to catch exceptions")
	def test_delete_none_existing_item_from_store(self):  # 5.1-2   can't check for permissions
		service.delete_item(33, self.user.pk)
