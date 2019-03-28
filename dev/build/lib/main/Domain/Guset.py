from main.domain.User import User


class Guest(User):

	def __init__(self, tradingSystem):
		User.__init__(self, tradingSystem=tradingSystem)

	def login(self, username, password):
		return False
