from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from guardian.shortcuts import assign_perm
from selenium import webdriver

from store.models import Store


class MyUnitTesting(StaticLiveServerTestCase):
	default_password = "q2w44r32c1"
	default_user = "qqq"
	default_store = "rrr"
	driver = None

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.driver = webdriver.Chrome()

	@classmethod
	def tearDownClass(cls):
		cls.driver.close()
		super().tearDownClass()

	def setUp(self) -> None:
		super().setUp()
		self.user = User.objects.create(username=self.default_user, password=make_password(self.default_password))
		self.store = Store.objects.create(name=self.default_store, description="bla bla bla")
		self.store.owners.add(self.user)
		assign_perm('ADD_ITEM', self.user, self.store)
		assign_perm('REMOVE_ITEM', self.user, self.store)
		assign_perm('EDIT_ITEM', self.user, self.store)
		assign_perm('ADD_MANAGER', self.user, self.store)

	# def tearDown(self) -> None:
	# 	self.driver.close()

	def login(self, user, password):
		self.driver.get(self.live_server_url + "/accounts/login/")
		self.driver.find_element_by_name("username").send_keys(user)
		element = self.driver.find_element_by_name("password")
		element.send_keys(password)
		element.submit()
