from django.contrib.auth.models import User, Group
from django.db.models import Q
from guardian.shortcuts import assign_perm

from store.models import Store, Item, BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule
from trading_system.models import ObserverUser, Cart


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


def add_complex_rule_to_store_2(rule1, parameter1, rule2, parameter2, store_id, operator1, operator2, prev_rule):
	store = Store.objects.get(id=store_id)
	if rule1 == 'MAX_QUANTITY' or rule1 == 'MIN_QUANTITY':
		try:
			int(parameter1)
			if int(parameter1) > 0:
				pass
			else:
				return [False, 'Enter a positive number please for first parameter']
		except ValueError:
			return [False, 'Enter a number please for first parameter']
	if rule2 == 'MAX_QUANTITY' or rule2 == 'MIN_QUANTITY':
		try:
			int(parameter2)
			if int(parameter2) > 0:
				pass
			else:
				return [False, 'Enter a positive number please for second parameter']
		except ValueError:
			return [False, 'Enter a number please for second parameter']
	baseRule1 = BaseRule(store=store, type=rule1, parameter=parameter1)
	baseRule1.save()
	rule_id1 = baseRule1.id
	rule1_temp = '_' + str(rule_id1)
	baseRule2 = BaseRule(store=store, type=rule2, parameter=parameter2)
	baseRule2.save()
	rule_id2 = baseRule2.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexStoreRule(left=rule1_temp, right=rule2_temp, operator=operator1, store=store)
	cr.save()
	cr_id = cr.id
	cr2 = ComplexStoreRule(left=prev_rule, right=cr_id, operator=operator2, store=store)
	cr2.save()
	return [True, cr2.id]


def add_base_rule_to_item(item_id, rule, parameter):
	item = Item.objects.get(id=item_id)
	brule = BaseItemRule(item=item, type=rule, parameter=parameter)
	brule.save()
	return [True, brule.id]


def add_complex_rule_to_item_1(item_id, prev_rule, rule, operator, parameter):
	item = Item.objects.get(id=item_id)
	baseRule = BaseItemRule(item=item, type=rule, parameter=parameter)
	baseRule.save()
	rule_id2 = baseRule.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexItemRule(left=prev_rule, right=rule2_temp, operator=operator, item=item)
	cr.save()
	return [True, cr.id]


def add_complex_rule_to_item_2(item_id, prev_rule, rule1, parameter1, rule2, parameter2, operator1, operator2):
	item = Item.objects.get(id=item_id)
	baseRule1 = BaseItemRule(item=item, type=rule1, parameter=parameter1)
	baseRule1.save()
	rule_id1 = baseRule1.id
	rule1_temp = '_' + str(rule_id1)
	baseRule2 = BaseItemRule(item=item, type=rule2, parameter=parameter2)
	baseRule2.save()
	rule_id2 = baseRule2.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexItemRule(left=rule1_temp, right=rule2_temp, operator=operator1, item=item)
	cr.save()
	cr_id = cr.id
	cr2 = ComplexItemRule(left=prev_rule, right=cr_id, operator=operator2, item=item)
	cr2.save()
	return [True, cr2.id]


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
	return [True, 'store was deleted : ' + store.name]


def have_no_more_stores(user_pk):
	tmp = Store.objects.filter(owners__username__contains=user_pk)
	return len(tmp) == 0


def get_item_store(item_pk):
	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))
	# Might cause bug. Need to apply the item-in-one-store condition
	return stores[0]


def get_cart(store_pk, user_pk):
	carts = Cart.objects.filter(customer_id=user_pk, store_id=store_pk)
	if len(carts) == 0:
		return None
	else:
		return carts[0]


def open_cart_for_user_in_store(store_pk: int, user_pk: int) -> None:
	Cart(customer_id=user_pk, store_id=store_pk).save()


def add_item_to_cart(user_id, item_id):
	user = User.objects.get(pk=user_id)
	if (user.is_authenticated):
		item_store = get_item_store(item_id)
		cart = get_cart(item_store, user_id)
		if cart is None:
			open_cart_for_user_in_store(item_store.pk, user.pk)  # TODO
			cart = get_cart(item_store, user.pk)
		cart.items.add(item_id)
		return True
	return False


def get_item_store(item_pk):
	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))

	# Might cause bug. Need to apply the item-in-one-store condition
	return list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))[0]


def is_authenticated(user_id):
	return User.objects.get(pk=user_id).is_authenticated


def get_item(id):
	return Item.objects.get(id=id)


def amount_in_db(item_id):
	amount_in_db = Item.objects.get(id=item_id).quantity
	if (amount_in_db > 0):
		return True
	return False


def make_cart_2(item_id):
	item = Item.objects.get(id=item_id)
	amount_in_db = Item.objects.get(id=item_id).quantity
	item.quantity = amount_in_db - 1
	item.save()


def remove_item_from_cart(user_id, item_id):
	item = Item.objects.get(id=item_id)
	cart = Cart.objects.get(customer=User.objects.get(pk=user_id))
	cart.items.remove(item)
	if (item.quantity == 0):
		item.delete()


def user_has_cart_for_store(store_pk, user_pk):
	return len(Cart.objects.filter(customer_id=user_pk, store_id=store_pk)) > 0


def user_has_cart_for_store(store_pk: int, user_pk: int) -> bool:
	return len(Cart.objects.filter(customer_id=user_pk, store_id=store_pk)) > 0