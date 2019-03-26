from main.Domain.TradingSystemFacade import TradingSystemFacade


def test_watch_gc():
	facade = TradingSystemFacade()
	ownerSession = facade.initateSession()
	facade.register(ownerSession, "roy", "123456")
	facade.addStore(ownerSession, "RoysStore", "niceStore")
	facade.addItemToStore(ownerSession, storeId="RoysStore", itemName="bamba", desc="bamba is a food", price=12,
	                      amount=2)
	sessionId = facade.initiateSession()
	facade.addItemToCart(sessionId, 1, storeId="RoysStore", itemName="bamba")
	assert "[RoysStore, bamba]" == facade.watchCart(sessionId)
