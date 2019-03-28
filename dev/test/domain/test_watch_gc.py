from main.domain.DomainFacade import DomainFacade


def test_watch_gc():
	owner_session = DomainFacade.initiate_session()
	DomainFacade.register(session_id=owner_session, username="roy", password="123456")
	DomainFacade.add_store(owner_session, "RoysStore", "niceStore")
	DomainFacade.add_item_to_store(store_id="RoysStore", itemName="bamba", desc="bamba is a food",
	                               price=12,
	                               amount=2)
	session_id = DomainFacade.initiate_session()
	DomainFacade.add_item_to_cart(session_id=session_id, store_id="RoysStore", item_name="bamba")
	assert "[RoysStore, bamba]" == DomainFacade.watch_cart(session_id)
