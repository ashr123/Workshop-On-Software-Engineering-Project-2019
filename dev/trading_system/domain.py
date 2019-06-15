import datetime

from django.contrib.auth.models import User, Group
from django.db.models import Q
from guardian.shortcuts import assign_perm

from store.models import Store, Item, BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule, Discount
from trading_system.models import ObserverUser, Cart, NotificationUser, Notification


def add_manager(wanna_be_manager, picked, is_owner, store_pk, store_manager):
	messages_ = ''
	try:
		user_ = User.objects.get(username=wanna_be_manager)
	except:
		fail = True
		messages_ += 'no such user'
		return [fail, messages_]
	# messages.warning(request, 'no such user')
	# return redirect('/store/add_manager_to_store/' + str(store_pk) + '/')
	store_ = Store.objects.get(id=store_pk)
	if wanna_be_manager == store_manager:
		fail = True
		messages_ += 'can`t add yourself as a manager!'
		return [fail, messages_]
	# messages.warning(request, 'can`t add yourself as a manager!')
	# return redirect('/store/home_page_owner/')
	pre_store_owners = store_.owners.all()
	# print('\n owners: ' ,pre_store_owners)
	for owner in pre_store_owners:
		if owner.username == wanna_be_manager:
			fail = True
			messages_ += 'allready owner 1'
			return [fail, messages_]
	# messages.warning(request, 'allready owner')
	# return redirect('/store/home_page_owner/')

	if user_ is None:
		fail = True
		messages_ += 'No such user'
		return [fail, messages_]
	# messages.warning(request, 'No such user')
	# return redirect('/store/home_page_owner/')
	for perm in picked:
		assign_perm(perm, user_, store_)
	if is_owner:
		try:
			if store_.owners.filter(id=user_.pk).exists():
				return [True, 'allready owner 2']
			store_owners_group = Group.objects.get(name="store_owners")
			user_.groups.add(store_owners_group)
			store_.owners.add(user_)
			ObserverUser.objects.create(user_id=user_.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
		except:
			return [True, 'allready manager']
	else:
		try:
			if store_.managers.filter(id=user_.pk).exists():
				return [True, 'allready manager']
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
	return store.pk


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

def get_store_details(store_id):
	store = Store.objects.get(pk=store_id)
	items = list(map(lambda i: str(i),store.items.all()))
	owners = list(map(lambda o: User.objects.get(pk=o.id).username,store.owners.all()))
	managers = list(map(lambda m: User.objects.get(pk=m.id).username,store.managers.all()))
	return {"name": store.name, "description": store.description, "owners": owners, "managers": managers, "items": items}

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
	item = Item.objects.create(price=price, name=name, category=category, description=description, quantity=quantity)
	item.save()
	curr_store = Store.objects.get(id=store_id)
	curr_store.items.add(item)
	return [True, 'Your Item was added successfully!']


def can_remove_store(store_id, user_id):
	user = User.objects.get(pk=user_id)
	store = Store.objects.get(pk=store_id)
	return user.has_perm('REMOVE_STORE', store)
from itertools import chain

def delete_store(store_id):

	store = Store.objects.get(id=store_id)
	items_to_delete = store.items.all()
	owners = store.owners.all()
	managers = store.managers.all()
	owners_all =list(chain(owners,managers))
	store.delete()
	for item_ in items_to_delete:
		item_.delete()
	for owner in owners_all:
		tmp_ow = Store.objects.filter(owners__id__contains=owner.username)
		print('yyyyyyyyyyyyyyyyyyyyyyy',tmp_ow )
		print('++++++++++++++++++++++++++++++++++++++++++++',owner)
		if have_no_more_stores(owner.id):
			owners_group = Group.objects.get(name="store_owners")
			managers_group = Group.objects.get_or_create(name="store_managers")
			managers_group = Group.objects.get(name="store_managers")
			# user = User.objects.get(id = owner)
			managers_group.user_set.remove(owner)
			owners_group.user_set.remove(owner)
	return [True, 'store was deleted : ' + store.name]




def have_no_more_stores(user_pk):
	print('oooooooooooooooooooooooooo',user_pk)

	owner_of_stores = Store.objects.filter(owners__id__in=[user_pk])
	manager_of_stores = Store.objects.filter(managers__id__in=[user_pk])
	# tmp_ow = Store.objects.filter(owners__id__contains=user_pk)
	# tmp_man = Store.objects.filter(managers__id__contains=user_pk)
	tmp = list(chain(owner_of_stores,manager_of_stores))
	print('ppppppppppppppppppppppppppppppppppppp',len(tmp) == 0)
	return len(tmp) == 0



def get_user_store_list(user_id):
	user = User.objects.get(pk=user_id)
	if "store_managers" in user.groups.values_list('name', flat=True):
		user_stores = Store.objects.filter(managers__id__in=[user_id])
	else:
		user_stores = Store.objects.filter(owners__id__in=[user_id])
	return list(map(lambda s: {'id': s.pk, 'name': s.name}, user_stores))


def get_item_details(item_id):
	item = Item.objects.get(pk = item_id)
	return {"name": item.name,
	        "category": item.get_category_display,
	        "description": item.description,
	        "price": item.price,
	        "quantity": item.quantity}
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


def open_cart_for_user_in_store(store_pk, user_pk):
	Cart(customer_id=user_pk, store_id=store_pk).save()


def add_item_to_cart(user_id, item_id):
	if user_id ==None:
		user = User.objects.filter(username='AnonymousUser')[0]
	else:
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


def user_has_cart_for_store(store_pk, user_pk):
	return len(Cart.objects.filter(customer_id=user_pk, store_id=store_pk)) > 0


def len_of_super():
	return len(User.objects.filter(is_superuser=True))

def add_discount(store_id,  percentage,  end_date, type=None, amount=None, item=None):
	store = Store.objects.get(id=store_id)
	discount = Discount(store=store, type=type, percentage=percentage, amount=amount, end_date=end_date, item=item)
	discount.save()
	return [True, discount.id]

def update_item(item_id, item_dict):
	item = Item.objects.get(pk = item_id)
	for field in item._meta.fields:
		if field.attname in item_dict.keys():
			setattr(item, field.attname, item_dict[field.attname])
	item.save()
	return True

def item_rules_string(itemId):
	base_arr = []
	complex_arr = []
	base = []
	complex = []
	item = Item.objects.get(id=itemId)
	itemRules = ComplexItemRule.objects.all().filter(item=item)
	for rule in reversed(itemRules):
		if rule.id in complex_arr:
			continue
		res = {"id": rule.id, "type": 2, "item": itemId, "name": string_item_rule(rule, base_arr, complex_arr)}
		complex.append(res)
	itemBaseRules = BaseItemRule.objects.all().filter(item=item)
	for rule in itemBaseRules:
		if rule.id in base_arr:
			continue
		res = {"id": rule.id, "type": 1, "item": itemId, "name": get_base_rule_item(rule.id)}
		base.append(res)
	return complex + base

def string_item_rule(rule, base_arr, complex_arr):
	curr = '('
	if rule.left[0] == '_':
		base_arr.append(int(rule.left[1:]))
		curr += get_base_rule_item(int(rule.left[1:]))
	else:
		complex_arr.append(int(rule.left))
		tosend = ComplexItemRule.objects.get(id=int(rule.left))
		curr += string_item_rule(tosend, base_arr, complex_arr)
	curr += ' ' + rule.operator + ' '
	if rule.right[0] == '_':
		base_arr.append(int(rule.right[1:]))
		curr += get_base_rule_item(int(rule.right[1:]))
	else:
		complex_arr.append(int(rule.right))
		tosend = ComplexItemRule.objects.get(id=int(rule.right))
		curr += string_item_rule(tosend, base_arr, complex_arr)
	curr += ')'
	return curr

def get_base_rule_item(rule_id):
	rule = BaseItemRule.objects.get(id=rule_id)
	return rule.type + ': ' + rule.parameter

def store_rules_string(store_id):
	base_arr = []
	complex_arr = []
	base = []
	complex = []
	storeRules = ComplexStoreRule.objects.all().filter(store_id= store_id)
	for rule in reversed(storeRules):
		if rule.id in complex_arr:
			continue
		res = {"id": rule.id, "type": 2, "store": store_id, "name": string_store_rule(rule, base_arr, complex_arr)}
		complex.append(res)
	storeBaseRules = BaseRule.objects.all().filter(store_id= store_id)
	for rule in storeBaseRules:
		if rule.id in base_arr:
			continue
		res = {"id": rule.id, "type": 1, "store": store_id, "name": get_base_rule(rule.id)}
		base.append(res)
	return complex + base

def string_store_rule(rule, base_arr, complex_arr):
	curr = '('
	if rule.left[0] == '_':
		base_arr.append(int(rule.left[1:]))
		curr += get_base_rule(int(rule.left[1:]))
	else:
		complex_arr.append(int(rule.left))
		tosend = ComplexStoreRule.objects.get(id=int(rule.left))
		curr += string_store_rule(tosend, base_arr, complex_arr)
	curr += ' ' + rule.operator + ' '
	if rule.right[0] == '_':
		base_arr.append(int(rule.right[1:]))
		curr += get_base_rule(int(rule.right[1:]))
	else:
		complex_arr.append(int(rule.right))
		tosend = ComplexStoreRule.objects.get(id=int(rule.right))
		curr += string_store_rule(tosend, base_arr, complex_arr)
	curr += ')'
	return curr

def get_base_rule(rule_id):
	rule = BaseRule.objects.get(id=rule_id)
	if rule.type == "REG":
		return rule.type + ': Only'
	return rule.type + ': ' + rule.parameter


def get_store_items(store_id):
	store = Store.objects.get(pk = store_id)
	items = store.items.all()
	return list(map(lambda i: i.__dict__,items))

def get_store_managers(store_id):
	store = Store.objects.get(pk = store_id)
	managers = store.managers.all()
	return list(map(lambda i: i.__dict__,managers))

def get_store_owners(store_id):
	store = Store.objects.get(pk = store_id)
	owners = store.owners.all()
	return list(map(lambda i: i.__dict__,owners))


def update_store(store_id, store_dict):
	store = Store.objects.get(pk=store_id)
	for field in store._meta.fields:
		if field.attname in store_dict.keys():
			setattr(store, field.attname, store_dict[field.attname])
	store.save()
	return True

def get_discount_for_store(pk, amount, total):
	store_of_item = Store.objects.get(items__id__contains=pk)
	if not (len(store_of_item.discounts.all()) == 0):
		discount_ = store_of_item.discounts.all()[0]
		now = datetime.datetime.now().date()
		if (discount_.end_date >= now):
			conditions = discount_.conditions.all()
			if (len(conditions) > 0):
				for cond in conditions:
					if (amount <= cond.max_amount and amount >= cond.min_amount):
						percentage = discount_.percentage
						total = (100 - percentage) / 100 * float(total)
						str_ret = percentage
						return [str_ret, total]
			else:
				percentage = discount_.percentage
				total = (100 - percentage) / 100 * float(total)
				str_ret = percentage
				return [str_ret, total]
	else:
		return [0, total]

def get_discount_for_item(pk, amount, total):
	item = Item.objects.get(id=pk)
	if not (len(item.discounts.all()) == 0):
		item_discount = item.discounts.all()[0]
		now = datetime.datetime.now().date()
		if (item_discount.end_date >= now):
			conditions_item = item_discount.conditions.all()
			if (len(conditions_item) > 0):
				for cond_i in conditions_item:
					if (amount <= cond_i.max_amount and amount >= cond_i.min_amount):
						percentage = item_discount.percentage
						total = (100 - percentage) / 100 * float(total)
						str_ret = percentage
						return [str_ret, total]
			else:
				percentage = item_discount.percentage
				total = (100 - percentage) / 100 * float(total)
				str_ret = percentage
				return [str_ret, total]
	else:
		return [0, total]


def delete_item(item_id):
	item = Item.objects.get(pk = item_id)
	item.delete()
	return True


def get_store_creator(store_id):
	store = Store.objects.get(pk= store_id)
	return store.owners.all()[0]  # creator


def get_store_by_id(store_id):
	return Store.objects.get(pk= store_id)

def remove_manager_from_store(store_id,m_id):
	store_ = Store.objects.get(pk= store_id)
	store_.managers.remove(id =m_id)

def remove_manager_from_store(store_id,m_id):
	try:
		store_ = Store.objects.get(pk= store_id)
		user = User.objects.get(id =m_id)
		is_manager = len(Store.objects.filter(id=store_id,owners__id__in=[m_id]))==0
		if (is_manager):
			store_.managers.remove(user)
			return True
		else:
			store_.owners.remove(user)
			return True
	except:
		return False



def get_user_notifications(user_id):
	user_ntfcs = NotificationUser.objects.filter(user=user_id)
	ntfcs_ids = list(map(lambda n: n.notification_id, user_ntfcs))
	ntfcs = list(map(lambda pk: Notification.objects.get(id=pk), ntfcs_ids))
	return list(map(lambda n: n.__dict__,ntfcs))


def mark_notification_read(user_id):
	for n in NotificationUser.objects.filter(user=user_id):
		n.been_read = True
		n.save()
	return True