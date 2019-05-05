from dev.mainTest import MyUnitTesting
from store.models import Store


class StoreUnitTesting(MyUnitTesting):
	def test_add_store(self):
		store_name = "check"
		self.login(user=self.default_user, password=self.default_password)
		self.driver.get(self.live_server_url + "/store/add_store/")
		self.driver.find_element_by_name("name").send_keys(store_name)
		element = self.driver.find_element_by_name("description")
		element.send_keys("bli bli bli")
		element.submit()
		self.assertTrue(Store.objects.filter(name=store_name).exists())

	def test_add_item(self):
		self.driver.find_element_by_value()
