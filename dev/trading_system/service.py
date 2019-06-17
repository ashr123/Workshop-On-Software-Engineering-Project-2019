import json

from trading_system.domain import domain


def search(txt):
	return domain.search(txt)


def add_manager(user_name, picked, is_owner, store_pk, request_user_name):
	"""

	:param user_name: 
	:param picked: 
	:param is_owner: 
	:param store_pk: 
	:param request_user_name: 
	:return: True if failing
	"""
	return domain.add_manager(user_name, picked, is_owner, store_pk, request_user_name)


def open_store(store_name, desc, user_id):
	return domain.open_store(store_name, desc, user_id)


def add_base_rule_to_store(rule_type, store_id, parameter, user_id):
	return domain.add_base_rule_to_store(rule_type, store_id, parameter, user_id)


def add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter, user_id):
	return domain.add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter, user_id)


def add_complex_rule_to_store_2(rule1, parameter1, rule2, parameter2, store_id, operator1, operator2, prev_rule,
                                user_id):
	return domain.add_complex_rule_to_store_2(rule1, parameter1, rule2, parameter2, store_id, operator1, operator2,
	                                          prev_rule, user_id)


def add_base_rule_to_item(item_id, rule, parameter, user_id):
	return domain.add_base_rule_to_item(item_id, rule, parameter, user_id)


def add_complex_rule_to_item_1(item_id, prev_rule, rule, operator, parameter, user_id):
	return domain.add_complex_rule_to_item_1(item_id, prev_rule, rule, operator, parameter, user_id)


def add_complex_rule_to_item_2(item_id, prev_rule, rule1, parameter1, rule2, parameter2, operator1, operator2, user_id):
	return domain.add_complex_rule_to_item_2(item_id, prev_rule, rule1, parameter1, rule2, parameter2, operator1,
	                                         operator2, user_id)


def add_item_to_store(item_json, store_id, user_id):
	item_dict = json.loads(item_json)
	return domain.add_item_to_store(price=item_dict['price'],
	                                name=item_dict['name'],
	                                description=item_dict['description'],
	                                category=item_dict['category'],
	                                quantity=item_dict['quantity'],
	                                store_id=store_id,
	                                user_id=user_id)


def can_remove_store(store_id, user_id):
	return domain.can_remove_store(store_id=store_id, user_id=user_id)


def have_no_more_stores(user_pk):
	return domain.have_no_more_stores(user_pk=user_pk)


def delete_store(store_id, user_id):
	return domain.delete_store(store_id=store_id, user_id=user_id)


def get_store_details(store_id):
	return domain.get_store_details(store_id=store_id)


def get_store_items(store_id):
	return domain.get_store_items(store_id=store_id)


def get_store_managers(store_id):
	return domain.get_store_managers(store_id=store_id)


def get_store_owners(store_id):
	return domain.get_store_owners(store_id=store_id)


def get_user_store_list(user_id):
	return domain.get_user_store_list(user_id=user_id)


def get_item_details(item_id):
	return domain.get_item_details(item_id=item_id)


def get_store_by_id(store_id):
	return domain.get_store_by_id(store_id)


def remove_manager_from_store(store_id, m_id):
	return domain.remove_manager_from_store(store_id, m_id)


def len_of_super():
	return domain.len_of_super()


def is_authenticated(user_id):
	return domain.is_authenticated(user_id)


def update_item(item_id, item_dict, user_id):
	return domain.update_item(item_id=item_id, item_dict=item_dict, user_id=user_id)


def add_discount(store_id, percentage, end_date, user_id, item=None, amount=None):
	return domain.add_discount(store_id=store_id, user_id=user_id, percentage=percentage, amount=amount,
	                           end_date=end_date,
	                           item=item)


def item_rules_string(itemId):
	return domain.item_rules_string(itemId)


def store_rules_string(store_id):
	return domain.store_rules_string(store_id)


def update_store(store_id, store_dict):
	return domain.update_store(store_id, store_dict)


def get_discount_for_store(pk, amount, total):
	return domain.get_discount_for_store(pk, amount, total)


def get_discount_for_item(pk, amount, total):
	return domain.get_discount_for_item(pk, amount, total)


def delete_item(item_id, user_id):
	return domain.delete_item(item_id, user_id=user_id)


def get_store_creator(store_id):
	return domain.get_store_creator(store_id)


def get_user_notifications(user_id):
	return domain.get_user_notifications(user_id)


def mark_notification_read(user_id):
	return domain.mark_notification_read(user_id)


def add_item_to_cart(user_id, item_id):
	return domain.add_item_to_cart(user_id, item_id)


def get_item(id1):
	return domain.get_item(id1)


def add_complex_discount(store_id, left, right, operator):
	return domain.add_complex_discount_to_store(store_id, left, right, operator)


def buy_logic(item_id, amount, user_id, shipping_details, card_details):
	return domain.buy_logic(item_id, amount, user_id, shipping_details, card_details)
