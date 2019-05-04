from django.contrib.auth.models import User
from selenium import webdriver
from django.contrib.auth.hashers import make_password
# from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase


# class TestCase(DTestCase):
# 	multi_db = True


class UnitTesting(LiveServerTestCase):

	def setUp(self):
		self.driver = webdriver.Chrome()

	def tearDown(self):
		self.driver.close()

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
		# user = User.objects.filter(username=user)[0]
		self.assertTrue(User.objects.filter(username=user).exists())

		self.driver.get(self.live_server_url + "/accounts/signup/")
		self.driver.find_element_by_name("username").send_keys(user)
		self.driver.find_element_by_name("password1").send_keys(password)
		element = self.driver.find_element_by_name("password2")
		element.send_keys(password)
		element.submit()
		self.assertTrue("A user with that username already exists." in self.driver.page_source)

	def test_login(self):
		password = "q2w44r32c1"
		user = "qqq"
		User.objects.create(username=user, password=make_password(password))
		self.driver.get(self.live_server_url + "/accounts/login/")
		self.driver.find_element_by_name("username").send_keys(user)
		element = self.driver.find_element_by_name("password")
		element.send_keys(password)
		element.submit()
		# user1 = User.objects.filter(username=user)[0].is_authenticated
		self.assertTrue(User.objects.filter(username=user)[0].is_authenticated)