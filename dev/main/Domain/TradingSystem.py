from .TradingSystemException import UserAlreadyExistException
from .TradingSystemException import PermissionException
from .Guset import Guest
from .Member import Member
from main.security import  SecureLogIn


class TradingSystem(object):

    def __init__(self):
        self._users = {}
        self._members = []
        self._stores = []

    def get_user(self, session_id):
        return "h"

    def get_member(self, member_name):
        if member_name in map(lambda member: member.name, self._members):
            return filter(lambda member: member.name == member_name, self._members)[0]
        return None

    def genarate_id(self):
        newSessionId = len(self._users)
        self._users[newSessionId] = Guest(tradingSystem=self)
        return newSessionId

    def search(self, keyword):
        return False

    def registerMember(self, sessionId, username, password):
        if username in map(lambda m: m.name, self._members):
            raise UserAlreadyExistException(message="the user {} is already registered".format(username))
        self._members[sessionId] = Member(username)  # TODO - handle security

    def login(self, sessionId, username, password):
        if not username in map(lambda m: m.name, self._members):
            raise PermissionException(message="the user {} is not a member !".format(username))

        self._members[sessionId] = Member(username)  # TODO - handle security
