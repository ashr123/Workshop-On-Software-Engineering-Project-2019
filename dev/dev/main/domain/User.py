from dev.main.domain.Item import Item
from dev.main.domain.TradingSystemException import UnImplementedException


class User(object):
	def buy_item(self, item):
		return False

	def add_item_to_cart(self, item: Item, store_name: str):
		raise UnImplementedException("add_item_to_cart: Not implemented!")

	def watch_gc(self):
		raise UnImplementedException("watch_gc: Not implemented!")
