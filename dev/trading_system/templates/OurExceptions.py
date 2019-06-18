class DBFailedExceptionDomainToService(Exception):
	def __init__(self, msg = None):
		self.msg = msg

class DBFailedExceptionServiceToViews(Exception):
	def __init__(self, msg = None):
		self.msg = msg