import datetime

from django.contrib.auth.models import User, Group
from django.db.models import Q

from store.models import BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule, Discount
# from store.models import Item, BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule, Discount
from trading_system.models import ObserverUser, NotificationUser, Notification
from trading_system.domain.store import Store as c_Store
from trading_system.domain.user import User as c_User
from trading_system.domain.item import Item as c_Item
from trading_system.domain.cart import Cart as c_Cart


def add_manager(wanna_be_manager, picked, is_owner, store_pk, store_manager):
	messages_ = ''
	try:
		user_ = User.objects.get(username=wanna_be_manager)
	except:
		fail = True
		messages_ += 'no such user'
		return [fail, messages_]
	store = c_Store.get_store(store_id=store_pk)
	if wanna_be_manager == store_manager:
		fail = True
		messages_ += 'can`t add yourself as a manager!'
		return [fail, messages_]
	# messages.warning(request, 'can`t add yourself as a manager!')
	# return redirect('/store/home_page_owner/')
	pre_store_owners_ids = store.all_owners_ids()
	# print('\n owners: ' ,pre_store_owners)
	for owner_id in pre_store_owners_ids:
		if c_User.get_user(user_id=owner_id).username == wanna_be_manager:
			fail = True
			messages_ += 'allready owner'
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
		store.assign_perm(perm=perm, user_id=user_.pk)
	if is_owner:
		try:
			if store.is_already_owner(user_id=user_.pk):
				return [True, 'allready owner']
			store_owners_group = Group.objects.get(name="store_owners")
			user_.groups.add(store_owners_group)
			# store_.owners.add(user_)
			store.add_owner(user_.pk)
			ObserverUser.objects.create(user_id=user_.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
		except:
			return [True, 'allready manager']
	else:
		try:
			if store.is_already_manager(user_id=user_.pk):
				return [True, 'allready manager']
			store_managers = Group.objects.get_or_create(name="store_managers")[0]
			# store_managers = Group.objects.get(name="store_managers")
			user_.groups.add(store_managers)
			store.add_manager(user_.pk)
			ObserverUser.objects.create(user_id=user_.pk,
			                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
		except:
			return [True, 'allready manager ']

	return [False, '']


def search(txt):
	return c_Item.search(txt=txt)


def open_store(store_name, desc, user_id):
	store = c_Store(name=store_name, desc=desc, owner_id=user_id)
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
	brule = BaseRule(store_id=store_id, type=rule_type, parameter=parameter)
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
	base_rule = BaseRule(store_id=store_id, type=rule_type, parameter=parameter)
	base_rule.save()
	rule_id2 = base_rule.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexStoreRule(left=prev_rule, right=rule2_temp, operator=operator, store_id=store_id)
	cr.save()
	return [True, cr.id]


def get_store_details(store_id):
	return c_Store.get_store(store_id).get_details()


def add_complex_rule_to_store_2(rule1, parameter1, rule2, parameter2, store_id, operator1, operator2, prev_rule):
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
	base_rule1 = BaseRule(store_id=store_id, type=rule1, parameter=parameter1)
	base_rule1.save()
	rule_id1 = base_rule1.id
	rule1_temp = '_' + str(rule_id1)
	base_rule2 = BaseRule(store_id=store_id, type=rule2, parameter=parameter2)
	base_rule2.save()
	rule_id2 = base_rule2.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexStoreRule(left=rule1_temp, right=rule2_temp, operator=operator1, store_id=store_id)
	cr.save()
	cr_id = cr.id
	cr2 = ComplexStoreRule(left=prev_rule, right=cr_id, operator=operator2, store_id=store_id)
	cr2.save()
	return [True, cr2.id]


def add_base_rule_to_item(item_id, rule, parameter):
	brule = BaseItemRule(item_id=item_id, type=rule, parameter=parameter)
	brule.save()
	return [True, brule.id]


def add_complex_rule_to_item_1(item_id, prev_rule, rule, operator, parameter):
	base_rule = BaseItemRule(item_id=item_id, type=rule, parameter=parameter)
	base_rule.save()
	rule_id2 = base_rule.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexItemRule(left=prev_rule, right=rule2_temp, operator=operator, item_id=item_id)
	cr.save()
	return [True, cr.id]


def add_complex_rule_to_item_2(item_id, prev_rule, rule1, parameter1, rule2, parameter2, operator1, operator2):
	base_rule1 = BaseItemRule(item_id=item_id, type=rule1, parameter=parameter1)
	base_rule1.save()
	rule_id1 = base_rule1.id
	rule1_temp = '_' + str(rule_id1)
	base_rule2 = BaseItemRule(item_id=item_id, type=rule2, parameter=parameter2)
	base_rule2.save()
	rule_id2 = base_rule2.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexItemRule(left=rule1_temp, right=rule2_temp, operator=operator1, item_id=item_id)
	cr.save()
	cr_id = cr.id
	cr2 = ComplexItemRule(left=prev_rule, right=cr_id, operator=operator2, item_id=item_id)
	cr2.save()
	return [True, cr2.id]


def add_item_to_store(price, name, description, category, quantity, store_id):
	item = c_Item(price=price, name=name, category=category, description=description, quantity=quantity)
	c_Store.get_store(store_id).add_item(item_pk=item.pk)
	return [True, 'Your Item was added successfully!']


def can_remove_store(store_id, user_id):
	return c_Store.get_store(store_id=store_id).has_perm(perm='REMOVE_STORE', user_id=user_id)


def delete_store(store_id):
	s = c_Store.get_store(store_id)
	s.delete()
	return [True, 'store was deleted : ' + s.name]


def get_user_store_list(user_id):
	return c_User.get_user(user_id=user_id).get_stores()


def get_item_details(item_id):
	return c_Item.get_item(item_id=item_id).get_details()



def add_item_to_cart(user_id, item_id):
	user = c_User.get_user(user_id=user_id)
	if user.is_authenticated():
		item_store_pk = c_Store.get_item_store(item_pk=item_id).pk
		cart = c_Cart.get_cart(store_pk=item_store_pk, user_id=user.pk)
		if cart is None:
			cart = c_Cart(store_pk=item_store_pk, user_pk=user_id)
		cart.add_item(item_id=item_id)
		return True
	return False


def is_authenticated(user_id):
	return c_User.get_user(user_id=user_id).is_authenticated()


def amount_in_db(item_id):
	return c_Item.get_item(item_id=item_id).quantity > 0


# TODO - FOR WHAT PURPOSE
def make_cart_2(item_id):
	item = Item.objects.get(id=item_id)
	item.quantity = Item.objects.get(id=item_id).quantity - 1
	item.save()


def remove_item_from_cart(user_id, item_id):
	c_Cart.get_cart(user_id=user_id).remove_item(item_id=item_id)
	item = c_Item.get_item(id=item_id)
	if item.quantity == 0:
		item.delete()


def user_has_cart_for_store(store_pk, user_pk):
	return c_Cart.get_cart(store_pk=store_pk, user_id=user_pk) != None


def len_of_super():
	return c_User.len_of_super()


def add_discount(store_id, percentage, end_date, kind=None, amount=None, item=None):
	discount = Discount(store_id=store_id, type=type, percentage=percentage, amount=amount,
	                    end_date=end_date, item=item)
	discount.save()
	return [True, discount.id]


def update_item(item_id, item_dict):
	c_Item.get_item(item_id=item_id).update(item_dict=item_dict)
	return True


def item_rules_string(item_id):
	base_arr = []
	complex_arr = []
	base = []
	complex1 = []
	# item = Item.objects.get(id=item_id)
	for rule in reversed(ComplexItemRule.objects.all().filter(item_id=item_id)):
		if rule.id in complex_arr:
			continue
		res = {"id": rule.id, "type": 2, "item": item_id, "name": string_item_rule(rule, base_arr, complex_arr)}
		complex1.append(res)
	for rule in BaseItemRule.objects.all().filter(item_id=item_id):
		if rule.id in base_arr:
			continue
		res = {"id": rule.id, "type": 1, "item": item_id, "name": get_base_rule_item(rule.id)}
		base.append(res)
	return complex1 + base


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
	complex1 = []
	for rule in reversed(ComplexStoreRule.objects.all().filter(store_id=store_id)):
		if rule.id in complex_arr:
			continue
		res = {"id": rule.id, "type": 2, "store": store_id, "name": string_store_rule(rule, base_arr, complex_arr)}
		complex1.append(res)
	for rule in BaseRule.objects.all().filter(store_id=store_id):
		if rule.id in base_arr:
			continue
		res = {"id": rule.id, "type": 1, "store": store_id, "name": get_base_rule(rule.id)}
		base.append(res)
	return complex1 + base


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
	return list(
		map(lambda i_d: c_Item.get_item(item_id=i_d).to_dict(), c_Store.get_store(store_id=store_id).all_items_ids()))


def get_store_managers(store_id):
	store = Store.objects.get(pk=store_id)
	managers = store.managers.all()
	return list(map(lambda i: i.__dict__, managers))


def get_store_owners(store_id):
	store = Store.objects.get(pk=store_id)
	owners = store.owners.all()
	return list(map(lambda i: i.__dict__, owners))


def update_store(store_id, store_dict):
	c_Store.get_store(store_id=store_id).update(store_dict=store_dict)
	return True


# TODO - EXTRACT STORE
def get_discount_for_store(pk, amount, total):
	store_of_item = Store.objects.get(items__id__contains=pk)
	if not (len(store_of_item.discounts.all()) == 0):
		discount_ = store_of_item.discounts.all()[0]
		if discount_.end_date >= datetime.datetime.now().date():
			conditions = discount_.conditions.all()
			if len(conditions) > 0:
				for cond in conditions:
					if cond.max_amount >= amount >= cond.min_amount:
						percentage = discount_.percentage
						total = (100 - percentage) / 100 * float(total)
						return [percentage, total]
			else:
				percentage = discount_.percentage
				total = (100 - percentage) / 100 * float(total)
				return [percentage, total]
	else:
		return [0, total]


# TODO - STOP USING ITEM
def get_discount_for_item(pk, amount, total):
	item = Item.objects.get(id=pk)
	if not (len(item.discounts.all()) == 0):
		item_discount = item.discounts.all()[0]
		if item_discount.end_date >= datetime.datetime.now().date():
			conditions_item = item_discount.conditions.all()
			if len(conditions_item) > 0:
				for cond_i in conditions_item:
					if cond_i.max_amount >= amount >= cond_i.min_amount:
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
	c_Item.get_item(item_id=item_id).delete()
	return True


def get_store_creator(store_id):
	return c_Store.get_store(store_id=store_id).get_creator().pk


def get_store_by_id(store_id):
	return Store.objects.get(pk=store_id)


def remove_manager_from_store(store_id, m_id):
	try:
		store_ = Store.objects.get(pk=store_id)
		user = User.objects.get(id=m_id)
		if len(Store.objects.filter(id=store_id, owners__id__in=[m_id])) == 0:
			store_.managers.remove(user)
			return True
		else:
			store_.owners.remove(user)
			return True
	except:
		return False


def get_user_notifications(user_id):
	return list(map(lambda n: n.__dict__, list(map(lambda pk: Notification.objects.get(id=pk),
	                                               list(map(lambda n: n.notification_id,
	                                                        NotificationUser.objects.filter(user=user_id)))))))


def mark_notification_read(user_id):
	for n in NotificationUser.objects.filter(user=user_id):
		n.been_read = True
		n.save()
	return True


def have_no_more_stores(user_pk):
	return c_User.get_user(user_id=user_pk).have_no_more_stores()
