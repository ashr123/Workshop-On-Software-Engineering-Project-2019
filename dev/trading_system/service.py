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
	return domain.add_base_rule_to_store(rule_type, prev_rule, store_id, operator, parameter)

