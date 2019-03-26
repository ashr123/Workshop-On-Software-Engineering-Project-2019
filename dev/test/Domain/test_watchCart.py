from main.Domain.TradingSystemFacade import TradingSystemFacade


def test_watchCart():
    print("hey")
    ts =  TradingSystemFacade.TradingSystemFacade()
    sessionID = ts.initateSession()
    ts.addItem(sessionID, "123")
    assert "123, bamba" in ts.watchCart()
