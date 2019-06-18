from django.db.models import Q

from store.models import Store as m_Store, Item
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm

from trading_system.models import ObserverUser
from trading_system.domain.user import User as c_User


class Store():
	def __init__(self, name=None, desc=None, owner_id=None, model=None):
		if model != None:
			self._model = model
			return
		self._model = m_Store.objects.create(name=name, description=desc)
		self._model.owners.add(User.objects.get(pk=owner_id))
		self._model.save()
		_user = User.objects.get(pk=owner_id)
		my_group = Group.objects.get_or_create(name="store_owners")[0]
		# my_group = Group.objects.get(name="store_owners")
		if len(ObserverUser.objects.filter(user_id=_user.pk)) == 0:
			ObserverUser.objects.create(user_id=_user.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(_user.pk)).save()
		_user.groups.add(my_group)
		assign_perm('ADD_ITEM', _user, self._model)
		assign_perm('REMOVE_ITEM', _user, self._model)
		assign_perm('EDIT_ITEM', _user, self._model)
		assign_perm('ADD_MANAGER', _user, self._model)
		assign_perm('REMOVE_STORE', _user, self._model)
		assign_perm('ADD_DISCOUNT', _user, self._model)

	@property
	def pk(self):
		return self._model.pk

	@property
	def name(self):
		return self._model.name

	def all_owners_ids(self):
		owners = list(self._model.owners.all())
		return list(map(lambda o: o.id, owners))

	def all_managers_ids(self):
		managers = list(self._model.managers.all())
		return list(map(lambda m: m.id, managers))

	def all_items_ids(self):
		items = list(self._model.items.all())
		return list(map(lambda i: i.id, items))

	def add_item(self, item_pk):
		item = Item.objects.get(pk=item_pk)
		self._model.items.add(item)

	def assign_perm(self, perm, user_id):
		assign_perm(perm, User.objects.get(pk=user_id), self._model)

	def has_perm(self, perm, user_id):
		return User.objects.get(pk=user_id).has_perm('REMOVE_STORE', self._model)

	def is_already_owner(self, user_id):
		return self._model.owners.filter(id=user_id).exists()

	def is_already_manager(self, user_id):
		return self._model.managers.filter(id=user_id).exists()

	def add_owner(self, user_id):
		self._model.owners.add(User.objects.get(pk=user_id))

	def add_manager(self, user_id):
		self._model.managers.add(User.objects.get(pk=user_id))

	def delete(self):
		items_to_delete = self._model.items.all()
		owners_ids = self.all_owners_ids()
		managers_ids = self.all_managers_ids()
		owners_objs = list(map(lambda id: c_User.get_user(user_id=id), owners_ids))
		managers_objs = list(map(lambda id: c_User.get_user(user_id=id), managers_ids))
		self._model.delete()
		for item_ in items_to_delete:
			item_.delete()
		for owner in owners_objs:
			if owner.owns_no_more_stores():
				owner.remove_from_owners()
		for manager in managers_objs:
			if manager.manages_no_more_stores():
				manager.remove_from_managers()

	def update(self, store_dict):
		for field in self._model._meta.fields:
			if field.attname in store_dict.keys():
				setattr(self._model, field.attname, store_dict[field.attname])


		self._model.save()

	def get_details(self):
		return {"name": self._model.name, "description": self._model.description, "owners":
			list(map(lambda o_id: User.objects.get(pk=o_id).username, self.all_owners_ids())), "managers":
			        list(map(lambda m_id: User.objects.get(pk=m_id).username, self.all_managers_ids())),
		        "items": list(map(lambda i_id: str(Item.objects.get(pk=i_id)), self.all_items_ids()))}

	def get_creator(self):
		return c_User(self._model.owners.all()[0])

	@staticmethod
	def get_store(store_id):
		return Store(model=m_Store.objects.get(pk=store_id))

	@staticmethod
	def owns_stores(user_id):
		tmp = m_Store.objects.filter(owners__username__contains=user_id)
		return len(tmp) == 0

	@staticmethod
	def manages_stores(user_id):
		tmp = m_Store.objects.filter(managers__username__contains=user_id)
		return len(tmp) == 0

	@staticmethod
	def get_owned_stores(user_id):
		return list(map(lambda s: {'id': s.pk, 'name': s.name},
		                m_Store.objects.filter(Q(managers__id__in=[user_id]) | Q(owners__id__in=[user_id]))))

	@staticmethod
	def get_item_store(item_pk):
		model = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), m_Store.objects.all()))[0]
		return Store(model=model)
