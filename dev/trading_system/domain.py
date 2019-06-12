from django.contrib.auth.models import User, Group
from django.db.models import Q
from guardian.shortcuts import assign_perm

from store.models import Store, Item
from trading_system.models import ObserverUser


def add_manager(user_name, picked, is_owner, pk, request_user_name):
	messages_ = ''
	try:
		user_ = User.objects.get(username=user_name)
	except:
		fail = True
		messages_ += 'no such user'
		return [fail, messages_]
	# messages.warning(request, 'no such user')
	# return redirect('/store/add_manager_to_store/' + str(pk) + '/')
	store_ = Store.objects.get(id=pk)
	if user_name == request_user_name:
		fail = True
		messages_ += 'can`t add yourself as a manager!'
		return [fail, messages_]
	# messages.warning(request, 'can`t add yourself as a manager!')
	# return redirect('/store/home_page_owner/')
	pre_store_owners = store_.owners.all()
	# print('\n owners: ' ,pre_store_owners)
	for owner in pre_store_owners:
		if (owner.username == user_name):
			fail = True
			messages_ += 'allready owner'
			return [fail, messages_]
		# messages.warning(request, 'allready owner')
		# return redirect('/store/home_page_owner/')

	if (user_ == None):
		fail = True
		messages_ += 'No such user'
		return [fail, messages_]
	# messages.warning(request, 'No such user')
	# return redirect('/store/home_page_owner/')
	for perm in picked:
		assign_perm(perm, user_, store_)
	if (is_owner):
		try:
			if store_.owners.get(id=user_.pk):
				print('hhhhhhhhhhhhhhh')
			store_owners_group = Group.objects.get(name="store_owners")
			user_.groups.add(store_owners_group)
			store_.owners.add(user_)
			ObserverUser.objects.create(user_id=user_.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
		except:
			return [True, 'allready manager']
	else:
		try:
			if store_.managers.get(id=user_.pk):
				print('hhhhhhhhhhhhhhh')
			store_managers = Group.objects.get_or_create(name="store_managers")
			store_managers = Group.objects.get(name="store_managers")
			user_.groups.add(store_managers)
			store_.managers.add(user_)
			ObserverUser.objects.create(user_id=user_.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
		except:
			return [True, 'allready manager ']

	return [False, '']

def search(txt):
	return Item.objects.filter(Q(name__contains=txt) | Q(
		description__contains=txt) | Q(
		category__contains=txt))


def open_store(store_name, desc, user_id):
	store = Store.objects.create(name=store_name,description=desc)
	store.owners.add(User.objects.get(pk= user_id))
	store.save()
	_user = User.objects.get(pk= user_id)
	my_group = Group.objects.get_or_create(name="store_owners")
	my_group = Group.objects.get(name="store_owners")
	if len(ObserverUser.objects.filter(user_id=_user.pk)) == 0:
		ObserverUser.objects.create(user_id=_user.pk,
		                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(_user.pk)).save()
	_user.groups.add(my_group)
	assign_perm('ADD_ITEM', _user, store)
	assign_perm('REMOVE_ITEM', _user, store)
	assign_perm('EDIT_ITEM', _user, store)
	assign_perm('ADD_MANAGER', _user, store)
	assign_perm('REMOVE_STORE', _user, store)
	assign_perm('ADD_DISCOUNT', _user, store)
	return 'Your Store was added successfully!'