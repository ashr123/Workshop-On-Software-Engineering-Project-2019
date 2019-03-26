class User(object):
	def __init__(self, tradingSystem):
		self._tradingSystem = tradingSystem

	def buyItem(self, item):
		return False

	def saveItemInGC(self, item):
		return False

	def watchGC(self):
		return str(self._groceryCarts)
