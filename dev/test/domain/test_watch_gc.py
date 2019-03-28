from main.Domain.DomainFacade import DomainFacade


def test_watch_gc():
	facade = DomainFacade()
	owner_session = facade.initateSession()
	facade.register(owner_session, "roy", "123456")
	facade.add_store(owner_session, "RoysStore", "niceStore")
	facade.addItemToStore(sessionId=owner_session, storeId="RoysStore", itemName="bamba", desc="bamba is a food",
	                      price=12,
	                      amount=2)
	sessionId = facade.initateSession()
	facade.addItemToCart(sessionId=sessionId, storeId="RoysStore", itemName="bamba")
	assert "[RoysStore, bamba]" == facade.watchCart(sessionId)
