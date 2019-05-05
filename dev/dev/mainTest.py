from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from store.models import Store


class MyUnitTesting(StaticLiveServerTestCase):
	default_password = "q2w44r32c1"
	default_user = "qqq"
	default_store = "rrr"

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.user = User.objects.create(username=cls.default_user, password=make_password(cls.default_password))
		cls.store = Store.objects.create(name=cls.default_store, description="bla bla bla", owner=cls.user)

	@classmethod
	def tearDownClass(cls):
		super().tearDownClass()

	def setUp(self) -> None:
		self.driver = webdriver.Chrome()

	def tearDown(self) -> None:
		self.driver.close()

	def login(self, user, password):
		self.driver.get(self.live_server_url + "/accounts/login/")
		self.driver.find_element_by_name("username").send_keys(user)
		element = self.driver.find_element_by_name("password")
		element.send_keys(password)
		element.submit()
