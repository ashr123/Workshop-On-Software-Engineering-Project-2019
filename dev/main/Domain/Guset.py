from main.Domain.User import User

class Guest(User):

    def __init__(self):
        pass

    def login(self, username, password):
        return False