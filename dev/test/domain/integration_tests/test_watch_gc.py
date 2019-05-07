from main.domain.DomainFacade import DomainFacade


def test_watch_gc():
    owner_session = DomainFacade.initiate_session()
    DomainFacade.register(session_id=owner_session, username="roy", password="123456")
    DomainFacade.login(session_id=owner_session, username="roy", password="123456")
    DomainFacade.add_store(owner_session, "RoysStore", "niceStore ffffffffffffffffffffffffff", [])
    DomainFacade.add_item_to_store(owner_session, "RoysStore", "bamba", 'Food', "bamba is a food", 12, 2)
    session_id = DomainFacade.initiate_session()
    DomainFacade.add_item_to_cart(session_id, "bamba", "RoysStore")
    assert "RoysStore: bamba 1 12\n" == DomainFacade.watch_cart(session_id)
