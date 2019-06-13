import json

from trading_system import domain


def buy_item():
	pass

def search(txt):
	return domain.search(txt)

def add_manager(user_name, picked, is_owner, pk, request_user_name):
	return domain.add_manager(user_name, picked, is_owner, pk, request_user_name)

def open_store(store_name, desc, user_id):
	return domain.open_store(store_name, desc, user_id)

def add_base_rule_to_store(rule_type, store_id, parameter):
	return domain.add_base_rule_to_store(rule_type, store_id, parameter)

def add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter):
	return domain.add_complex_rule_to_store_1(rule_type, prev_rule, store_id, operator, parameter)

def add_item_to_store(item_json, store_id):
	item_dict = json.loads(item_json)
	return domain.add_item_to_store(
		price=item_dict['price'],
		name=item_dict['name'],
		description=item_dict['description'],
		category=item_dict['category'],
		quantity=item_dict['quantity'],
		store_id=store_id)


def can_remove_store(store_id, user_id):
	return domain.can_remove_store(store_id=store_id, user_id= user_id)


def have_no_more_stores(owner_name):
	return domain.have_no_more_stores(user_pk=owner_name)


def delete_store(store_id):
	return domain.delete_store(store_id=store_id)