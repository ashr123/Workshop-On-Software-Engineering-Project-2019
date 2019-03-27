from passlib.hash import pbkdf2_sha512


class SecureLogIn(object):
	def __init__(self):
		self.passwords = {}

	def add_user_password(self, user_name: str, password: str) -> None:
		self.passwords[user_name] = pbkdf2_sha512.hash(password)

	def verifying(self, user_name: str, password: str) -> bool:
		return pbkdf2_sha512.verify(password, self.passwords[user_name])


#
# sec = SecureLogIn()
# sec.add_user_password("Roy", "BabaYaga")
# print(sec.passwords)
# print(sec.verifying("Roy", "Babayaga"))
# print(sec.verifying("Roy", "BabaYaga"))
