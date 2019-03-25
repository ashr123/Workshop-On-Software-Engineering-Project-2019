class TradingSystem(object):




	def __init__(self, users, managers, stores):
		self._users = users
		self._stores = stores
		self._managers = managers

	def get_user(self, session_id):
		return _users.get(session_id)

	def genarate_id(self):
		return len(_users)+1

	def search(self, keyword):
		return False
