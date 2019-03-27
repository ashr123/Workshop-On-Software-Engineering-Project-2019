class TradingSystemException(Exception):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class UserAlreadyExistException(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class UserAlreadyHasStoreException(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class GuestCannotOpenStoreException(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class AnomalyException(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class PermissionException(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)


class RegistrationExeption(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)
