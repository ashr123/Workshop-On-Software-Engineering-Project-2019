from passlib.hash import pbkdf2_sha512
from typing import Dict

passwords: Dict[str, str] = {}


class Security(object):
	@staticmethod
	def add_user_password(user_name: str, password: str) -> bool:
		if user_name in passwords.keys():
			return False
		passwords[user_name] = pbkdf2_sha512.hash(password)

	@staticmethod
	def verify(user_name: str, password: str) -> bool:
		return pbkdf2_sha512.verify(password, passwords[user_name])

	@staticmethod
	def clear_pass_dict() -> None:
		passwords.clear()

# Example
# sec = Security()
# sec.add_user_password("Roy", "BabaYaga")
# print(sec.passwords)
# print(sec.verify("Roy", "Babayaga"))
# print(sec.verify("Roy", "BabaYaga"))
