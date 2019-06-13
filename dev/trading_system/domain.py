from django.contrib.auth.models import User, Group
from django.db.models import Q
from guardian.shortcuts import assign_perm

from store.models import Store, Item, BaseRule, ComplexStoreRule
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
	store = Store.objects.create(name=store_name, description=desc)
	store.owners.add(User.objects.get(pk=user_id))
	store.save()
	_user = User.objects.get(pk=user_id)
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


def add_base_rule_to_store(rule_type, store_id, parameter):
	if rule_type == 'MAX_QUANTITY' or rule_type == 'MIN_QUANTITY':
		try:
			int(parameter)
			if int(parameter) > 0:
				pass
			else:
				# messages.warning(request, 'Enter a number please')
				return [False, 'Enter a positive number please']
		except ValueError:
			# messages.warning(request, 'Enter a number please')
			return [False, 'Enter a number please']
		# return redirect('/store/home_page_owner/')
	brule = BaseRule(store=Store.objects.get(id=store_id), type=rule_type, parameter=parameter)
	brule.save()
	return [True, brule.id]


def add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter):
	if rule_type == 'MAX_QUANTITY' or rule_type == 'MIN_QUANTITY':
		try:
			int(parameter)
			if int(parameter) > 0:
				pass
			else:
				return [False, 'Enter a positive number please']
		except ValueError:
			return [False, 'Enter a number please']
	store = Store.objects.get(id=store_id)
	baseRule = BaseRule(store=store, type=rule_type, parameter=parameter)
	baseRule.save()
	rule_id2 = baseRule.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexStoreRule(left=prev_rule, right=rule2_temp, operator=operator, store=store)
	cr.save()
	return [True, cr.id]


def add_item_to_store(price, name, description, category, quantity, store_id):
	item = Item.objects.create(price=price, name=name, description=description, quantity=quantity)
	item.save()
	curr_store = Store.objects.get(id=store_id)
	curr_store.items.add(item)
	return [True, 'Your Item was added successfully!']


def can_remove_store(store_id, user_id):
	user = User.objects.get(pk=user_id)
	store = Store.objects.get(pk=store_id)
	return user.has_perm('REMOVE_STORE', store)

def delete_store(store_id):
	store = Store.objects.get(id=store_id)
	items_to_delete = store.items.all()
	owner_name = store.owners.all()[0]  # craetor
	for item_ in items_to_delete:
		item_.delete()
	if have_no_more_stores(owner_name):
		owners_group = Group.objects.get(name="store_owners")
		user = User.objects.get(username=owner_name)
		owners_group.user_set.remove(user)
	return [True, 'store was deleted : '+store.name]

def have_no_more_stores(user_pk):
	tmp = Store.objects.filter(owners__username__contains=user_pk)
	return len(tmp) == 0