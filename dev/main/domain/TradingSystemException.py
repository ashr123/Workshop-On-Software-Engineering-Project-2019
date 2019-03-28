class TradingSystemException(Exception):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)
		self._message = message

	@property
	def msg(self):
		return self._message


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


class OpenStoreExeption(TradingSystemException):
	def __init__(self, message, errors=None):
		super().__init__(message, errors)

class PasswordToShortException(TradingSystemException):
	def __init__(self, errors=None):
		super().__init__("password must have 6 alpha-numeric characters", errors)
