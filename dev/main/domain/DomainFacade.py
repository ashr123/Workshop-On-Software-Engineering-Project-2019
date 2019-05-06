from functools import reduce
from typing import List, Optional

from main.CollectionSystemBridge import Facade as MoneyCollectionFacade
from main.SupplySystemBridge import Facade as ProductSupplyFacade
from main.ConsistencySystemBridge import Facade as ConsistencyRulesFacade
from main.domain.ManagementState import ManagementState
from main.domain.Permission import Permissions
from .TradingSystem import TradingSystem
from .Member import Member
from .TradingSystemException import *
from main.domain import Store
from main.domain import Item

import logging
log_setup = logging.getLogger('event log')
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fileHandler = logging.FileHandler('event.log', mode='a')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log_setup.setLevel(logging.INFO)
log_setup.addHandler(fileHandler)
log_setup.addHandler(streamHandler)
log_setup1 = logging.getLogger('error log')
fileHandler1 = logging.FileHandler('error.log', mode='a')
fileHandler1.setFormatter(formatter)
streamHandler1 = logging.StreamHandler()
streamHandler1.setFormatter(formatter)
log_setup1.setLevel(logging.ERROR)
log_setup1.addHandler(fileHandler1)
log_setup1.addHandler(streamHandler1)
logev = logging.getLogger('event log')
loger = logging.getLogger('error log')


class DomainFacade(object):
    _money_collection_handler = MoneyCollectionFacade.MoneyCollectionFacade()
    _supply_handler = ProductSupplyFacade.SupplyFacade()
    _consistency_handler = ConsistencyRulesFacade.ConsistencyFacade()

    @staticmethod
    def clear():
        TradingSystem.clear()
        DomainFacade._money_collection_handler.make_sys_pass()
        DomainFacade.make_consistency_pass()
        DomainFacade.make_supply_pass()

    @staticmethod
    def initiate_session():
        return TradingSystem.generate_id()

    @staticmethod
    def login(session_id: int, username: str, password: str):
        try:
            TradingSystem.login(session_id, username, password)
            return True
        except PermissionException as e:
            return e.msg

    @staticmethod
    def logout(session_id: int):
        try:
            TradingSystem.logout(session_id)
            return "OK"
        except PermissionException as e:
            return e.msg

    @staticmethod
    def register(session_id: int, username: str, password: str):
        try:
            TradingSystem.register_member(session_id, username, password)
            return True
        except RegistrationExeption as e:
            return e.msg

    @staticmethod
    def search_item(name: str = None, category=None, hashtag=None, fil_price=None, fil_rankStore=None,
                    fil_category=None, fil_rankItem=None):
        stores_to_relevant_item = dict(
            (store.name, store.search_item(name, category, hashtag, fil_price, fil_category, fil_rankItem))
            for store in TradingSystem._stores)
        stores_filtered_by_rank = dict((k, v) for k, v in stores_to_relevant_item.items() if
                                       fil_rankStore == None or TradingSystem.get_store(k).rank >= fil_rankStore)
        return reduce(lambda acc, curr: acc + list(map(lambda i: str(i), stores_filtered_by_rank[curr])),
                      stores_filtered_by_rank, [])

    @staticmethod
    def watch_cart(session_id: int):
        user = TradingSystem.get_user(session_id)
        if user is None:
            return "session id isn't valid"
        basket = user.watch_gc()
        to_return = ''
        for cart in basket.values():
            to_return += cart.store_name + ': '
            for item in cart.items:
                to_return += item.name + ' ' + str(cart.items[item]) + ' ' + str(cart.items[item] * item.price) + ', '
            to_return = to_return[0: -2]
            to_return += '\n'
        return to_return

    @staticmethod
    def add_item_to_cart(session_id: int, item_name: str, store_name: str):
        user = TradingSystem.get_user(session_id)
        if user is None:
            return "unrecognized user"
        try:
            item = TradingSystem.get_item(item_name, store_name)
        except TradingSystemException as e:
            return e.msg
        user.add_item_to_cart(item, store_name)
        return "OK"

    @staticmethod
    def remove_item_from_cart(session_id, item_name, store_name):
        user = TradingSystem.get_user(session_id)
        if user is None:
            return "unrecognized user"
        try:
            item = TradingSystem.get_item(item_name, store_name)
        except TradingSystemException as e:
            return e.msg
        try:
            user.remove_item_from_cart(item, store_name)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def change_item_quantity_in_cart(session_id: int, item_name: str, store_name: str, quantity: int):
        user = TradingSystem.get_user(session_id)
        if user is None:
            return "unrecognized user"
        try:
            item = TradingSystem.get_item(item_name, store_name)
        except TradingSystemException as e:
            return e.msg
        try:
            user.change_item_quantity_in_cart(item, store_name, quantity)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def buy_single_item(sessionId: int, store_name: str, item_name: str, amount: int):
        try:
            if TradingSystem.reserve_item_from_store(sessionId, store_name, item_name, amount):
                trans_id = TradingSystem.createTransaction(sessionId, store_name)
                TradingSystem.add_item_to_trans(trans_id, item_name, amount)
                return trans_id
        except TradingSystemException as e:
            return e.msg

    @staticmethod
    def buy_many_items(sessionId, list_of_carts_to_buy):
        try:
            purchase = TradingSystem.createPurchase(sessionId)
            for cart in list_of_carts_to_buy:
                store = cart["store"]
                for item in cart["list_of_items"]:
                    TradingSystem.reserve_item_from_store(sessionId, store, item, TradingSystem.get_amount(sessionId, store, item))
                    TradingSystem.add_item_to_purch(purchase, store, item, TradingSystem.get_amount(sessionId, store, item))
            return purchase
        except TradingSystemException as e:
            return e.msg

    @staticmethod
    def add_store(session_id: int, name: str, desc: str, rules) -> str:
        try:
            member: Member = TradingSystem.get_user_if_member(session_id)
            if member is None:
                raise GuestCannotOpenStoreException("Guset has no permission to open a store")
            if DomainFacade._consistency_handler.is_valid(rules) is False:
                raise AnomalyException("bundle of rules is not valid")
            if member.open_store(session_id=session_id, store_name=name, desc=desc, rules=rules):
                return "OK"
        except UserAlreadyHasStoreException as e:
            return e.msg
        except GuestCannotOpenStoreException as e:
            return e.msg
        except OpenStoreExeption as e:
            return e.msg
        logev.info("A new store was opened named %s", name)
        return "OK"

    @staticmethod
    def add_item_to_store(session_id: int, store_name: str, item_name: str, category: str, desc: str, price: float,
                          amount: int):
        manager: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
        if manager is None:
            return "guest can't add items from store"
        state: ManagementState = manager.get_store_management_state(store_name)
        if state is None:
            return "member {} is not a manager of this store".format(manager.name)
        try:
            return state.add_item(item_name, desc, category, price, amount)
        except TradingSystemException as e:
            return e.msg

    @staticmethod
    def remove_item_from_store(session_id: int, item_id: int, store_name: str):
        manager: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
        if manager is None:
            return "guest can't remove item from store"
        state: ManagementState = manager.get_store_management_state(store_name)
        if state is None:
            return "member {} is not a manager of this store".format(manager.name)
        try:
            state.remove_item(item_id)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def change_item_in_store(session_id, item_name, store_name, field, value):
        manager: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
        if manager is None:
            return "guest can't edit items from store"
        state: ManagementState = manager.get_store_management_state(store_name)
        if state is None:
            return "member {} is not a manager of this store".format(manager.name)
        try:
            item = TradingSystem.get_item(item_name, store_name)
            state.edit_item(item, field, value)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def add_owner(session_id: int, ownered_name: str, store_name: str):
        member: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
        if member is None:
            return "guest can't nominate owners"
        try:
            member.add_owner(store_name=store_name, member_name=ownered_name)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def remove_owner(session_id: int, owner_name: str, store_name: str):
        member: Optional[Member] = TradingSystem.get_user_if_member(session_id=session_id)
        if member is None:
            return "guest can't remove owners"
        try:
            member.remove_owner(store_name=store_name, member_name=owner_name)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def add_manager(owner_id: int, manager_name: str, store_name: str, permissions: List[str]):
        member: Optional[Member] = TradingSystem.get_user_if_member(session_id=owner_id)
        if member is None:
            return "guest can't nominate managers"
        try:
            member.add_manager(store_name=store_name, member_name=manager_name,
                               permission_list=list(map(lambda permission: Permissions[permission], permissions)))
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def remove_manager(nominator: int, manager: str, store_name: str):
        member: Optional[Member] = TradingSystem.get_user_if_member(session_id=nominator)
        if member is None:
            return "guest can't remove managers"
        try:
            member.remove_manager(store_name=store_name, member_name=manager)
        except TradingSystemException as e:
            return e.msg
        return "OK"

    @staticmethod
    def remove_member(session_id: int, user_to_remove: str):
        manager = TradingSystem.get_user_if_member(session_id)
        if manager is None:
            return "Not a member!!"
        if TradingSystem.is_manager(manager):
            try:
                TradingSystem.remove_member(user_to_remove)
            except TradingSystemException as e:
                return e.msg
        logev.info("the user %s eas banned from the system", user_to_remove)
        return "OK"

    @staticmethod
    def setup(master_user, password):
        logev.info("Starting system set up")
        try:
            DomainFacade._money_collection_handler.connect()
            DomainFacade._supply_handler.connect()
            DomainFacade. _consistency_handler.connect()
            TradingSystem.register_master_member(master_user, password)
        except TradingSystemException as e:
            loger.error("Registration of system manager failed!")
            return e.msg
        except MoneyCollectionException as e:
            loger.error("Failed to connect to the money collection system")
            return e.msg
        except SupplyException as e:
            loger.error("Failed to connect to the supply system")
            return e.msg
        except ConsistencyException as e:
            loger.error("Failed to connect to the consistency system")
            return e.msg
        logev.info("System set up finished successfully")
        return True

    @staticmethod
    def get_member(session_id: int) -> Member:
        return TradingSystem.get_user(session_id)

    @staticmethod
    def get_store(session_id: int, store_name: str) -> Store:
        member = TradingSystem.get_user_if_member(session_id)
        if member is None:
            return None
        store_indicator = list(filter(lambda ms: ms.store.name == store_name, member.stores_managed_states))
        if len(store_indicator) == 0:
            return None
        return store_indicator[0].store

    @staticmethod
    def watch_trans(trans_id):
        return TradingSystem.watch_trans(trans_id)

    @staticmethod
    def supply(trans_id, address):
        try:
            trans = TradingSystem.get_trans(trans_id)
            TradingSystem.check_order(trans, address)
            if DomainFacade._supply_handler.supply(trans_id, trans.num_of_items, address):
                trans.supply_succ()
                return "OK"
        except TradingSystemException as e:
            TradingSystem.remove_trans(trans_id)
            return e.msg


    @staticmethod
    def pay(session_id, trans_id, creditcard, date, snum):
        price = TradingSystem.calculate_price(TradingSystem.get_trans(trans_id))
        try:
            if DomainFacade._money_collection_handler.pay(creditcard, date, snum, price):
                TradingSystem.get_trans(trans_id).pay_succ()
                TradingSystem.apply_trans(session_id, trans_id)
                return "OK"
        except TradingSystemException as e:
            TradingSystem.remove_trans(trans_id)
            return e.msg

    # for test
    @staticmethod
    def make_collection_pass():
        return DomainFacade._money_collection_handler.make_sys_pass()

    @staticmethod
    def make_collection_fail():
        return DomainFacade._money_collection_handler.make_sys_fail()

    @staticmethod
    def make_consistency_pass():
        return DomainFacade._consistency_handler.make_sys_pass()

    @staticmethod
    def make_consistency_fail():
        return DomainFacade._consistency_handler.make_sys_fail()

    @staticmethod
    def make_supply_pass():
        return DomainFacade._supply_handler.make_sys_pass()

    @staticmethod
    def make_supply_fail():
        return DomainFacade._supply_handler.make_sys_fail()

    @staticmethod
    def get_item_amount(store_name, item_name):
        return TradingSystem.get_item( item_name, store_name).quantity
