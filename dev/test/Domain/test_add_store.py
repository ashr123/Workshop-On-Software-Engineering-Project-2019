import pytest

from main.Domain.DomainFacade import DomainFacade

def test_valid_store_addition():
	facade = DomainFacade()
	session_id = facade.initateSession()
	facade.register(sessionId=session_id, username="roy", password="123456")
	assert facade.add_store(session_id, "RoysStore", "niceStore")
	store = facade.get_store(session_id, "RoysStore")
	assert not store == None
	assert store.name == "RoysStore"


