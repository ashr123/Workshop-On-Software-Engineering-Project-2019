from main.domain.DomainFacade import DomainFacade
from main.domain import Member


def test_add_item_to_store():
	new_store_name = "RoysStore"
	new_item_name = "bamba"
	facade = DomainFacade()
	session_id = facade.initiate_session()
	facade.register(session_id, "roy", "123456")
	facade.add_store(session_id, new_store_name, "niceStore")
	assert facade.add_item_to_store(sessionId=session_id, store_name=new_store_name, itemName=new_item_name, desc="cool item",
	                                price=12.5, amount=1)
	store = facade.get_store(session_id=session_id,)
