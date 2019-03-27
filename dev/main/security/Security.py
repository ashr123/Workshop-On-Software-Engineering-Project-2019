from passlib.hash import pbkdf2_sha512
from typing import Dict


class Security(object):
	_passwords: Dict[str, str] = {}

	@staticmethod
	def contains(key: str) -> bool:
		return key in Security._passwords.keys()

	@staticmethod
	def add_user_password(username: str, password: str) -> bool:
		if username in Security._passwords.keys():
			return False
		Security._passwords[username] = pbkdf2_sha512.hash(password)

	@staticmethod
	def verify(user_name: str, password: str) -> bool:
		return pbkdf2_sha512.verify(password, Security._passwords[user_name])

	@staticmethod
	def clear_pass_dict() -> None:
		Security._passwords.clear()

# Example
# sec = Security()
# sec.add_user_password("Roy", "BabaYaga")
# print(sec._passwords)
# print(sec.verify("Roy", "Babayaga"))
# print(sec.verify("Roy", "BabaYaga"))
