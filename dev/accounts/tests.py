# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class UnitTesting(StaticLiveServerTestCase):
	default_password = "q2w44r32c1"
	default_user = "qqq"
	driver = webdriver.Chrome()

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		User.objects.create(username=cls.default_user, password=make_password(cls.default_password))


	@classmethod
	def tearDownClass(cls):
		cls.driver.close()
		super().tearDownClass()

	def login(self, user, password):
		self.driver.get(self.live_server_url + "/accounts/login/")
		self.driver.find_element_by_name("username").send_keys(user)
		element = self.driver.find_element_by_name("password")
		element.send_keys(password)
		element.submit()

	def test_website_uploading(self):
		self.driver.get(self.live_server_url)
		self.assertIn("WeBuy", self.driver.title)


	def test_signup(self):
		password = "q2w44r32c1"
		user = "silvFire"
		self.driver.get(self.live_server_url + "/accounts/signup/")
		self.driver.find_element_by_name("username").send_keys(user)
		self.driver.find_element_by_name("password1").send_keys(password)
		element = self.driver.find_element_by_name("password2")
		element.send_keys(password)
		element.submit()
		# default_user = User.objects.filter(username=default_user)[0]
		self.assertTrue(User.objects.filter(username=user).exists())

		self.driver.get(self.live_server_url + "/accounts/signup/")
		self.driver.find_element_by_name("username").send_keys(user)
		self.driver.find_element_by_name("password1").send_keys(password)
		element = self.driver.find_element_by_name("password2")
		element.send_keys(password)
		element.submit()
		self.assertTrue("A user with that username already exists." in self.driver.page_source)

	def test_login(self):
		self.login(user=self.default_user, password=self.default_password)
		# user1 = User.objects.filter(username=default_user)[0].is_authenticated
		self.assertTrue(User.objects.filter(username=self.default_user)[0].is_authenticated)
