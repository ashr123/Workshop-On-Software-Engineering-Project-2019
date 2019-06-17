import datetime
import traceback

from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm

from external_systems.money_collector.payment_system import Payment
from external_systems.supply_system.supply_system import Supply
from store.models import BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule, Discount, Store, Item, \
	ComplexDiscount
from trading_system.domain.cart import Cart as c_Cart
from trading_system.domain.item import Item as c_Item
from trading_system.domain.store import Store as c_Store
from trading_system.domain.user import User as c_User
# from store.models import Item, BaseRule, ComplexStoreRule, BaseItemRule, ComplexItemRule, Discount
from trading_system.models import ObserverUser, NotificationUser, Notification
from trading_system.observer import ItemSubject

pay_system = Payment()
supply_system = Supply()

from store.models import WaitToAgreement, ManagersWhoWait


def add_manager(wanna_be_manager, picked, is_owner, store_pk, store_manager, is_partner):
	print('--------------------------------------------------------is_p----', is_partner)

	if not User.objects.get(username=store_manager).has_perm('ADD_MANAGER', Store.objects.get(id=store_pk)):
		return [True, "Store manager don't have the permission to add another manager"]
	messages_ = ''
	store = c_Store.get_store(store_id=store_pk)
	if (is_partner):

		all_partners = store.all_partners_ids()
		if (len(all_partners) > 1):  # there is other partner besids curr
			store_obj = Store.objects.get(id=store_pk)
			wanna_be_manager_user_obg = User.objects.get(username=wanna_be_manager)
			store_manager_user_obg = User.objects.get(username=store_manager)
			wait_obj = WaitToAgreement(user_to_wait=wanna_be_manager_user_obg, store=store_obj)
			wait_obj.save()
			for m_id in all_partners:
				pre_manager_user_obg = User.objects.get(id=m_id)
				m_obj = ManagersWhoWait(user_who_wait=pre_manager_user_obg)
				m_obj.save()
				wait_obj.managers_who_wait.add(m_obj)
			wait_obj_for_this_manager = wait_obj.managers_who_wait.get(
				user_who_wait=store_manager_user_obg)  # remove curr manager from wait list
			wait_obj.managers_who_wait.remove(wait_obj_for_this_manager)
			wait_obj.save()
			messages_ += ' . wait to approve partnership . '
			return [False, messages_]
		else:
			if approved_user_to_store_manager(wanna_be_manager, store_pk):
				return [False,'approved']
			else:
				return  [True,'can`t complete']

	try:
		user_ = User.objects.get(username=wanna_be_manager)
	except:
		fail = True
		messages_ += 'no such user'
		return [fail, messages_]

	if wanna_be_manager == store_manager:
		fail = True
		messages_ += 'can`t add yourself as a manager!'
		return [fail, messages_]
	# messages.warning(request, 'can`t add yourself as a manager!')
	# return redirect('/store/home_page_owner/')
	pre_store_owners_ids = store.all_owners_ids()
	pre_store_managers_ids = store.all_managers_ids()
	all_pre_m_o = pre_store_managers_ids + pre_store_owners_ids

	# print('\n owners: ' ,pre_store_owners)
	for owner_id in all_pre_m_o:
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
			store_owners_group = Group.objects.get(name="store_owners")
			user_.groups.add(store_owners_group)
			# store_.owners.add(user_)
			store.add_owner(user_.pk)
			try:
				ObserverUser.objects.create(user_id=user_.pk,
				                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
			except Exception as e:
				messages_ += str(e)

		except Exception as e:
			messages_ += str(e)
	else:
		try:
			store_managers = Group.objects.get_or_create(name="store_managers")[0]
			# store_managers = Group.objects.get(name="store_managers")
			user_.groups.add(store_managers)
			store.add_manager(user_.pk)
			try:
				ObserverUser.objects.create(user_id=user_.pk,
				                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(user_.pk)).save()
			except Exception as e:
				messages_ += str(e)

		except Exception as e:
			messages_ += str(e)
			return [True, messages_]

	return [False, messages_]


def approved_user_to_store_manager(wanna_be_manager, store_pk):
	try:
		store_obj = Store.objects.get(id=store_pk)
		wanna_be_manager_user_obg = User.objects.get(username=wanna_be_manager)
		store_obj.owners.add(User.objects.get(pk=wanna_be_manager_user_obg.id))
		store_obj.partners.add(User.objects.get(pk=wanna_be_manager_user_obg.id))
		store_obj.save()
		my_group = Group.objects.get_or_create(name="store_owners")[0]
		# my_group = Group.objects.get(name="store_owners")
		try:
			if len(ObserverUser.objects.filter(user_id=wanna_be_manager_user_obg.pk)) == 0:
				ObserverUser.objects.create(user_id=wanna_be_manager_user_obg.pk,
				                            address="ws://127.0.0.1:8000/ws/store_owner/{}/".format(
					                            wanna_be_manager_user_obg.pk)).save()
		except:
			pass
		wanna_be_manager_user_obg.groups.add(my_group)
		assign_perm('ADD_ITEM', wanna_be_manager_user_obg, store_obj)
		assign_perm('REMOVE_ITEM', wanna_be_manager_user_obg, store_obj)
		assign_perm('EDIT_ITEM', wanna_be_manager_user_obg, store_obj)
		assign_perm('ADD_MANAGER', wanna_be_manager_user_obg, store_obj)
		assign_perm('REMOVE_STORE', wanna_be_manager_user_obg, store_obj)
		assign_perm('ADD_DISCOUNT', wanna_be_manager_user_obg, store_obj)
		assign_perm('ADD_RULE', wanna_be_manager_user_obg, store_obj)
		store_obj.save()
		return True
	except:
		return False


def search(txt):
	return c_Item.search(txt=txt)


def open_store(store_name, desc, user_id):
	store = c_Store(name=store_name, desc=desc, owner_id=user_id)
	return store.pk


def add_base_rule_to_store(rule_type, store_id, parameter, user_id):
	if not User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to add base rule to store!"]

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


def add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter, user_id):
	if not User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to add complex rule to store!"]

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


def add_complex_rule_to_store_2(rule1, parameter1, rule2, parameter2, store_id, operator1, operator2, prev_rule,
                                user_id):
	if not User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to add complex rule to store!"]

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


def add_base_rule_to_item(item_id, rule, parameter, user_id):
	if not (Store.objects.filter(items__id=item_id).exists() and
	        User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.filter(items__id=item_id)[0])):
		return [False, "you don't have the permission to add base rule to store!"]

	brule = BaseItemRule(item_id=item_id, type=rule, parameter=parameter)
	brule.save()
	return [True, brule.id]


def add_complex_rule_to_item_1(item_id, prev_rule, rule, operator, parameter, user_id):
	if not (Store.objects.filter(items__id=item_id).exists() and
	        User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.filter(items__id=item_id)[0])):
		return [False, "you don't have the permission to add complex rule to store!"]

	base_rule = BaseItemRule(item_id=item_id, type=rule, parameter=parameter)
	base_rule.save()
	rule_id2 = base_rule.id
	rule2_temp = '_' + str(rule_id2)
	cr = ComplexItemRule(left=prev_rule, right=rule2_temp, operator=operator, item_id=item_id)
	cr.save()
	return [True, cr.id]


def add_complex_rule_to_item_2(item_id, prev_rule, rule1, parameter1, rule2, parameter2, operator1, operator2, user_id):
	if not (Store.objects.filter(items__id=item_id).exists() and
	        User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.filter(items__id=item_id)[0])):
		return [False, "you don't have the permission to add complex rule to store!"]

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


def add_item_to_store(price, name, description, category, quantity, store_id, user_id):
	if not User.objects.get(id=user_id).has_perm('ADD_ITEM', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to add an item!"]

	item = c_Item(price=price, name=name, category=category, description=description, quantity=quantity)
	c_Store.get_store(store_id).add_item(item_pk=item.pk)
	return [True, 'Your Item was added successfully!', item.pk]


def can_remove_store(store_id, user_id):
	return c_Store.get_store(store_id=store_id).has_perm(perm='REMOVE_STORE', user_id=user_id)


def delete_store(store_id, user_id):
	if not User.objects.get(id=user_id).has_perm('ADD_ITEM', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to delete the store!"]

	s = c_Store.get_store(store_id)
	s.delete()
	return [True, 'store was deleted : ' + s.name]


def get_user_store_list(user_id):
	return c_User.get_user(user_id=user_id).get_stores()


def get_item_details(item_id):
	return c_Item.get_item(item_id=item_id).get_details()


def add_item_to_cart(user_id, item_id):
	if not (user_id == None):
		item_store_pk = c_Store.get_item_store(item_pk=item_id).pk
		cart = c_Cart.get_cart(store_pk=item_store_pk, user_id=user_id)
		if cart is None:
			cart = c_Cart(store_pk=item_store_pk, user_pk=user_id)
		cart.add_item(item_id=item_id)
		return True
	else:

		return False


def get_item(id1):
	return Item.objects.get(id=id1)


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


def add_complex_discount_to_store(store_id, left, right, operator):
	d = ComplexDiscount(store_id=store_id, left=left, right=right, operator=operator)
	d.save()
	return [True, d.pk]


def add_discount(store_id, percentage, end_date, user_id, amount=None, item=None):
	if not User.objects.get(id=user_id).has_perm('ADD_DISCOUNT', Store.objects.get(pk=store_id)):
		return [False, "you don't have the permission to add discount to store!"]

	discount = Discount(store_id=store_id, type=type, percentage=percentage, amount=amount,
	                    end_date=end_date, item=item)
	discount.save()
	return [True, discount.id]


def update_item(item_id, item_dict, user_id):
	if not (Store.objects.filter(items__id=item_id).exists() and
	        User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.filter(items__id=item_id)[0])):
		return [False, "you don't have the permission to update an item!"]

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


def delete_item(item_id, user_id):
	if not (Store.objects.filter(items__id=item_id).exists() and
	        User.objects.get(id=user_id).has_perm('ADD_RULE', Store.objects.filter(items__id=item_id)[0])):
		return [False, "you don't have the permission to delete this item from the store!"]

	c_Item.get_item(item_id=item_id).delete()
	return True


def get_store_creator(store_id):
	return c_Store.get_store(store_id=store_id).get_creator().pk


def get_store_by_id(store_id):
	return Store.objects.get(pk=store_id)


# TODO - REFACTOR
def remove_manager_from_store(store_id, m_id):
	try:
		store_ = Store.objects.get(pk=store_id)
		user = User.objects.get(id=m_id)
		print('---------------remove manager : ', user.username)
		is_manager = len(Store.objects.filter(id=store_id, owners__id__in=[m_id])) == 0
		if (is_manager):
			store_.managers.remove(user)
			if have_no_more_stores(m_id):
				print('[[[[[[[[[[[[[[[[[[[[[')
				owners_group = Group.objects.get(name="store_owners")
				managers_group = Group.objects.get_or_create(name="store_managers")
				managers_group = Group.objects.get(name="store_managers")
				# user = User.objects.get(id = owner)
				managers_group.user_set.remove(user)
				owners_group.user_set.remove(user)
			return True
		else:
			store_.owners.remove(user)
			if have_no_more_stores(m_id):
				print('[[[[[[[[[999999999999999999[[[[[[[[[[[[')
				owners_group = Group.objects.get(name="store_owners")
				managers_group = Group.objects.get_or_create(name="store_managers")
				managers_group = Group.objects.get(name="store_managers")
				managers_group.user_set.remove(user)
				owners_group.user_set.remove(user)
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


def buy_logic(item_id, amount, amount_in_db1, user, shipping_details, card_details):
	pay_transaction_id = -1
	supply_transaction_id = -1
	messages_ = ''
	curr_item = Item.objects.get(id=item_id)
	if amount <= amount_in_db1:
		# print("good amount")
		total = amount * curr_item.price
		total_after_discount = total
		# check item rules
		if check_item_rules(curr_item, amount, user) is False:
			messages_ += "you can't buy due to item policies"
			return False, 0, 0, messages_
		store_of_item = Store.objects.get(items__id__contains=item_id)
		# check store rules
		if check_store_rules(store_of_item, amount, shipping_details['country'], user) is False:
			messages_ += "you can't buy due to store policies"
			return False, 0, 0, messages_
		total_after_discount = apply_discounts(store=store_of_item, curr_item=curr_item, amount=int(amount))

		try:
			if pay_system.handshake():
				print("pay hand shake")

				pay_transaction_id = pay_system.pay(str(card_details['card_number']), str(card_details['month']),
				                                    str(card_details['year']), str(card_details['holder']),
				                                    str(card_details['cvc']),
				                                    str(card_details['id']))
				if (pay_transaction_id == '-1'):
					messages_ += '\n' + 'can`t pay !'
					return False, 0, 0, messages_
			else:
				messages_ += '\n' + 'can`t connect to pay system!'
				return False, 0, 0, messages_
			if supply_system.handshake():
				print("supply hand shake")
				supply_transaction_id = supply_system.supply(str(shipping_details['name']),
				                                             str(shipping_details['address']),
				                                             str(shipping_details['city']),
				                                             str(shipping_details['country']),
				                                             str(shipping_details['zip']))
				if supply_transaction_id == '-1':
					chech_cancle = pay_system.cancel_pay(pay_transaction_id)
					messages_ += '\n' + 'can`t supply abort payment!'
					return False, 0, 0, messages_
			else:
				chech_cancle = pay_system.cancel_pay(pay_transaction_id)
				messages_ += '\n' + 'can`t connect to supply system abort payment!'
				return False, 0, 0, messages_

			curr_item.quantity = amount_in_db1 - amount
			curr_item.save()

			# store = get_item_store(_item.pk)

			try:
				item_subject = ItemSubject(curr_item.pk)
				if (user.is_authenticated):
					notification = Notification.objects.create(
						msg=user.username + ' bought ' + str(amount) + ' pieces of ' + curr_item.name)
					notification.save()
					item_subject.subject_state = item_subject.subject_state + [notification.pk]
				else:
					notification = Notification.objects.create(
						msg='A guest bought ' + str(amount) + ' pieces of ' + curr_item.name)
					notification.save()
					item_subject.subject_state = item_subject.subject_state + [notification.pk]
			except Exception as e:
				messages_ += 'cant connect websocket ' + str(e)

			_item_name = curr_item.name
			# print("reached herre")
			if curr_item.quantity == 0:
				curr_item.delete()

			messages_ += '\n' + 'Thank you! you bought ' + _item_name + '\n' + 'Total after discount: ' \
			             + str(total_after_discount) + ' $' + '\n' + 'Total before: ' + str(total) + ' $'
			return True, total, total_after_discount, messages_
		except Exception as a:
			# print(a)
			# print(str(a))
			traceback.print_exc()
			curr_item.quantity = amount_in_db1
			curr_item.save()

			if not (pay_transaction_id == -1):
				messages_ += '\n' + 'failed and aborted pay! please try again!'
				chech_cancle = pay_system.cancel_pay(pay_transaction_id)
			if not (supply_transaction_id == -1):
				messages_ += '\n' + 'failed and aborted supply! please try again!'
				chech_cancle_supply = supply_system.cancel_supply(supply_transaction_id)
			messages_ = "Exception! "  '  :  ' + str(a)
			return False, 0, 0, messages_
	else:
		messages_ = "no such amount for item : " + str(item_id) + '   messages_ : ' + messages_
		return False, 0, 0, messages_


def check_item_rules(item, amount, user):
	base_arr = []
	complex_arr = []
	itemRules = ComplexItemRule.objects.all().filter(item=item)
	for rule in reversed(itemRules):
		if rule.id in complex_arr:
			continue
		if check_item_rule(rule, amount, base_arr, complex_arr, user) is False:
			return False
	itemBaseRules = BaseItemRule.objects.all().filter(item=item)
	for rule in itemBaseRules:
		if rule.id in base_arr:
			continue
		if check_base_item_rule(rule.id, amount, user) is False:
			return False
	return True


def check_store_rules(store_of_item, amount, country, user):
	base_arr = []
	complex_arr = []
	storeRules = ComplexStoreRule.objects.all().filter(store=store_of_item)
	for rule in reversed(storeRules):
		if rule.id in complex_arr:
			continue
		if check_store_rule(rule, amount, country, base_arr, complex_arr, user) is False:
			return False
	storeBaseRules = BaseRule.objects.all().filter(store=store_of_item)
	for rule in storeBaseRules:
		if rule.id in base_arr:
			continue
		if check_base_rule(rule.id, amount, country, user) is False:
			return False
	return True


#
def check_store_rule(rule, amount, country, base_arr, complex_arr, user):
	if rule.left[0] == '_':
		base_arr.append(int(rule.left[1:]))
		left = check_base_rule(int(rule.left[1:]), amount, country, user)
		print('left')
		print(str(left))
	else:
		complex_arr.append(int(rule.left))
		tosend = ComplexStoreRule.objects.get(id=int(rule.left))
		left = check_store_rule(tosend, amount, country, base_arr, complex_arr, user)
	if rule.right[0] == '_':
		base_arr.append(int(rule.right[1:]))
		right = check_base_rule(int(rule.right[1:]), amount, country, user)
		print('right')
		print(str(right))
	else:
		complex_arr.append(int(rule.right))
		tosend = ComplexStoreRule.objects.get(id=int(rule.right))
		right = check_store_rule(tosend, amount, country, base_arr, complex_arr, user)
	if rule.operator == "AND" and (left == False or right == False):
		return False
	if rule.operator == "OR" and (left == False and right == False):
		return False
	if rule.operator == "XOR" and ((left == False and right == False) or (left == True and right == True)):
		return False
	return True


#
def check_item_rule(rule, amount, base_arr, complex_arr, user):
	if rule.left[0] == '_':
		base_arr.append(int(rule.left[1:]))
		left = check_base_item_rule(int(rule.left[1:]), amount, user)
	else:
		complex_arr.append(int(rule.left))
		tosend = ComplexItemRule.objects.get(id=int(rule.left))
		left = check_item_rule(tosend, amount, base_arr, complex_arr, user)
	if rule.right[0] == '_':
		base_arr.append(int(rule.right[1:]))
		right = check_base_item_rule(int(rule.right[1:]), amount, user)
	else:
		complex_arr.append(int(rule.right))
		tosend = ComplexItemRule.objects.get(id=int(rule.right))
		right = check_item_rule(tosend, amount, base_arr, complex_arr, user)
	if rule.operator == "AND" and (left == False or right == False):
		return False
	if rule.operator == "OR" and (left == False and right == False):
		return False
	if rule.operator == "XOR" and ((left == False and right == False) or (left == True and right == True)):
		return False
	return True


def check_base_item_rule(rule_id, amount, user):
	rule = BaseItemRule.objects.get(id=rule_id)
	if rule.type == 'MAX' and amount > int(rule.parameter):
		return False
	elif rule.type == 'MIN' and amount < int(rule.parameter):
		return False
	return True


def check_base_rule(rule_id, amount, country, user):
	rule = BaseRule.objects.get(id=rule_id)
	if rule.type == 'MAX' and amount > int(rule.parameter):
		return False
	elif rule.type == 'MIN' and amount < int(rule.parameter):
		return False
	elif rule.type == 'FOR' and country == rule.parameter:
		return False
	elif rule.type == 'REG' and not user.is_authenticated:
		return False
	return True


def apply_discounts(store, curr_item, amount):
	base_arr = []
	complex_arr = []
	price = curr_item.price * amount
	store_complex_discountes = ComplexDiscount.objects.filter(store=store)
	for disc in reversed(store_complex_discountes):
		if disc.id in complex_arr:
			continue
		price = apply_complex(disc, base_arr, complex_arr, curr_item, amount, price)
	store_base_discountes = Discount.objects.filter(store=store)
	for disc in store_base_discountes:
		if disc.id in base_arr:
			continue
		discount = float(apply_base(disc.id, curr_item, amount))
		print(price)
		print(discount)
		if (discount != -1):
			price = (1 - discount) * float(price)
	return price


def apply_complex(disc, base_arr, complex_arr, curr_item, amount, price):
	if disc.left[0] == '_':
		base_arr.append(int(disc.left[1:]))
		left = apply_base(int(disc.left[1:]), curr_item, amount)
	else:
		complex_arr.append(int(disc.left))
		tosend = ComplexStoreRule.objects.get(id=int(disc.left))
		left = apply_complex(tosend, base_arr, complex_arr, curr_item, amount, price)
	if disc.right[0] == '_':
		base_arr.append(int(disc.right[1:]))
		right = apply_base(int(disc.right[1:]), curr_item, amount)
	else:
		complex_arr.append(int(disc.right))
		tosend = ComplexStoreRule.objects.get(id=int(disc.right))
		right = apply_complex(tosend, base_arr, complex_arr, curr_item, amount, price)
	if disc.operator == "AND" and (left != -1 and right != -1):
		return (float(price) * float(left)) * float(right)
	elif disc.operator == "OR":
		if left != -1:
			price = left * price
		if right != -1:
			price = right * price
		return price
	elif disc.operator == "XOR":
		price1 = price
		price2 = price
		if left != -1:
			price1 = left * price
		if right != -1:
			price2 = right * price
		return min(price1, price2)


def apply_base(disc, curr_item, amount):
	base = Discount.objects.get(id=disc)
	per = float(base.percentage)
	today = datetime.date.today()
	if base.end_date < today:
		return -1
	if base.item == None:
		if base.type == 'MIN':
			if amount >= base.amount:
				return per / 100
			else:
				return -1
		if base.type == 'MAX':
			if amount <= base.amount:
				return per / 100
			else:
				return -1
		else:
			return per / 100
	elif base.item.id == curr_item.id:
		if base.type == 'MIN':
			if amount >= base.amount:
				return per / 100
			else:
				return -1
		if base.type == 'MAX':
			if amount <= base.amount:
				return per / 100
			else:
				return -1
		else:
			return per / 100
	else:
		print(curr_item.id)
		print(base.item.id)
		return -1
