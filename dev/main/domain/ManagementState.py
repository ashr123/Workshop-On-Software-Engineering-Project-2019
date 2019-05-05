from typing import List, Optional, Union

from main.domain.Permission import Permissions
from .Item import Item

from .TradingSystemException import PermissionException, AnomalyException
from .Store import Store
from main.domain import TradingSystem


class ManagementState(object):
    def __init__(self, is_owner: bool, permissions_list: List[Permissions], store: Store, nominator):
        self._isOwner: bool = is_owner
        self._permissions: List[Permissions] = permissions_list
        self._nominator = nominator
        self._store: Store = store

    @property
    def is_owner(self) -> bool:
        return self._isOwner

    @is_owner.setter
    def is_owner(self, is_owner: bool):
        _isOwner = is_owner

    @property
    def permissions(self) -> List[Permissions]:
        return self._permissions

    @property
    def store(self) -> Store:
        return self._store

    @property
    def nominator(self):
        return self._nominator

    def add_item(self, item_name: str, desc: str, category: str, price: float, amount: int) -> (str, int):
        if not self.is_owner and Permissions.ADD_ITEM not in self._permissions:
            raise PermissionException(message="you don't have the permission to do this action!")
        if self.store.search_item(name=item_name):
            raise AnomalyException("there is already item with this name in this store")
        if price <= 0:
            raise AnomalyException("price can't be non positive")
        if amount < 0 or isinstance(amount, float):
            raise AnomalyException("amount can't be negative integer")
        item_id: int = TradingSystem.TradingSystem.generate_item_id()
        self.store.add_item(Item(item_id, item_name, desc, category, price, amount))
        return "OK", item_id

    def remove_item(self, item_id: int):
        if not self.is_owner and Permissions.REMOVE_ITEM not in self._permissions:
            raise PermissionException(message="you don't have the permission to do this action!")
        if not self.store.remove_item(item_id):
            raise AnomalyException("no item with id {}".format(item_id))

    def edit_item(self, item, field, value):
        if not self.is_owner and Permissions.EDIT_ITEM not in self._permissions:
            raise PermissionException(message="you don't have the permission to do this auction!")
        return self.store.edit_item(item, field, value)

    def add_owner(self, member_name: str, nominator) -> None:
        if not self.is_owner:
            raise PermissionException(message="you don't have the permission to add owner!")
        new_owner = TradingSystem.TradingSystem.get_member(member_name=member_name)
        if new_owner is None:
            raise AnomalyException("member to be ownered doesn't exists")
        if len(list(filter(lambda state: state.store.name == self.store.name and state.is_owner,
                           new_owner.stores_managed_states))) > 0:
            raise PermissionException(message="you're already an owner of this store! (circular nomination)")
        existing_management_state: Optional[ManagementState] = new_owner.get_store_management_state(self.store.name)
        if existing_management_state is not None:
            existing_management_state.is_owner = True
        else:
            new_owner.add_managment_state(is_owner=True, permissions_list=[], store=self._store, nominator=nominator)
            self.store.add_owner(owner=new_owner)

    def remove_manager(self, manager_name: str, remover, is_master: bool) -> None:
        manager = TradingSystem.TradingSystem.get_member(member_name=manager_name)
        if manager is None:
            raise PermissionException(message="%s is not a manager of this store" %manager_name)
        existing_management_state: Optional[ManagementState] = manager.get_store_management_state(self.store.name)
        if not is_master and remover.name != existing_management_state._nominator.name:
            raise PermissionException(
                message="manager/owner can't remove another manager/owner that he didn't nominate")
        else:
            self.store.remove_manager(manager=manager)
            for child_of_manager in self.store.managers:
                manager_state: ManagementState = child_of_manager.get_store_management_state(self.store.name)
                manager_nominator = manager_state.nominator
                if manager_nominator is not None and manager_nominator.name == manager_name:
                    existing_management_state.remove_manager(child_of_manager.name, manager, is_master=is_master)
            manager.stores_managed_states.remove(existing_management_state)

    def add_manager(self, manager_name, permissions_list: List[Permissions], nominator) -> None:
        if Permissions.ADD_MANAGER not in self.permissions and not self.is_owner:
            raise PermissionException(message="you don't have the permission to add manager!")
        new_manager = TradingSystem.TradingSystem.get_member(member_name=manager_name)
        if new_manager is None:
            raise AnomalyException("member to be promoted doesn't exists")
        if len(list(filter(lambda state: state.store.name == self.store.name,
                           new_manager.stores_managed_states))) > 0:
            raise PermissionException(message="you're already a manager of this store! (circular nomination)")
        new_manager.add_managment_state(is_owner=False, permissions_list=permissions_list, store=self._store,
                                        nominator=nominator)
        self.store.add_owner(owner=new_manager)

    def set_manager_permissions(self, manager_id) -> bool:
        # if not self.permissions[8] == True:
        # 	raise PermissionException(message="you d'ont have the permission to do this auction !")
        return False
