
from passlib.hash import pbkdf2_sha256

class SecureLogIn(object):
    def __init__(self):
        self.passwords = {}

    def add_user_password(self, user ,password):
        self.passwords[user] = pbkdf2_sha256.hash(password)

    def verifying(self,user, password):
        hash_pass = self.passwords.get(user)
        return pbkdf2_sha256.verify(password, hash_pass)


