from main.Domain.DomainFacade import DomainFacade
from main.Domain import Member

def setup_module(module):
    pass

def teardown_module(module):
    pass

def test_register():
	facade = DomainFacade()
	session_id = facade.initateSession()
	assert facade.register(session_id, "roy", "123456")
	member = facade.get_member(session_id)
	assert not member == None
	assert member.name.__eq__("roy")