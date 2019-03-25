class User(object):
	def __init__(self, groceryCarts, tradingSystem):
		self._groceryCarts = groceryCarts
		self._tradingSystem = tradingSystem

	def buyItem(self, item):
		return False

	def saveItemInGC(self, item):
		return False

	def watchGC(self):
		return False
