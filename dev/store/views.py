import datetime
import json
import traceback

import simplejson as s_json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, redirect, render_to_response
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from guardian.decorators import permission_required_or_403

from trading_system import service
from trading_system.forms import SearchForm
from trading_system.models import Notification, NotificationUser
from trading_system.observer import ItemSubject
from . import forms
from .forms import BuyForm, AddManagerForm, AddRuleToItem, AddRuleToStore_base, AddRuleToStore_withop, \
	AddRuleToStore_two, AddDiscountForm
from .forms import ShippingForm, AddRuleToItem_withop, AddRuleToItem_two
from .models import Item, ComplexStoreRule, ComplexItemRule
from .models import Store


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def get_country_of_request(request):
	ip_ = get_client_ip(request)
	g = GeoIP2()
	return g.country_name(ip_)


@permission_required_or_403('ADD_ITEM', (Store, 'id', 'pk'))
@login_required
def add_item(request, pk):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			ans = service.add_item_to_store(item_json=s_json.dumps(form.cleaned_data),
			                                store_id=pk)
			messages.success(request, ans[1])  # <-
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, 'Problem with filed : ', form.errors, 'please try again!')  # <-
			return redirect('/store/home_page_owner/')
	else:
		form_class = ItemForm
		curr_store = Store.objects.get(id=pk)
		store_name = curr_store.name
		text = SearchForm()
		user_name = request.user.username
		context = {
			'store': pk,
			'form': form_class,
			'store_name': store_name,
			'user_name': user_name,
			'text': text,
		}
		# print('\ndebug\n\n', pk)
		return render(request, 'store/add_item.html', context)


# from ipware.ip import get_ip


@login_required
def add_store(request):
	user_groups = request.user.groups.values_list('name', flat=True)
	if "store_owners" in user_groups or "store_managers" in user_groups:
		base_template_name = 'store/homepage_store_owner.html'
	else:
		base_template_name = 'homepage_member.html'
	text = SearchForm()
	user_name = request.user.username
	set_input = forms.OpenStoreForm()
	context = {
		'set_input': set_input,
		'user_name': user_name,
		'text': text,
		'base_template_name': base_template_name
	}
	return render_to_response('store/add_store.html', context)


@login_required
def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		msg = service.open_store(store_name=open_store_form.cleaned_data.get('name'),
		                         desc=open_store_form.cleaned_data.get('description'),
		                         user_id=request.user.pk)
		messages.success(request, msg)
		return redirect('/store/home_page_owner')
	else:
		messages.warning(request, 'Please correct the error and try again.')  # <-
		return redirect('/login_redirect')


# need to be in the first time:

@method_decorator(login_required, name='dispatch')
class StoreDetailView(DetailView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		text = SearchForm()
		user_name = self.request.user.username
		context = {}
		details = service.get_store_details(kwargs['object'].pk)
		context['text'] = text
		context['user_name'] = user_name
		context['store'] = details
		return context


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context

	def get_queryset(self):
		if ("store_managers" in self.request.user.groups.values_list('name', flat=True)):
			return Store.objects.filter(managers__id__in=[self.request.user.id])
		else:
			return Store.objects.filter(owners__id__in=[self.request.user.id])


class ItemListView(ListView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		context['user_name'] = self.request.user.username
		return context

	def get_queryset(self):
		return service.get_store_items(store_id=self.kwargs['store_pk'])


class ItemDetailView(DetailView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = {
			'text': text,
			'item': service.get_item_details(item_id=kwargs['object'].pk)
		}
		return context


from .forms import UpdateItems, StoreForm, ItemForm


@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):
	model = Item
	# fields = ['name', 'owners', 'items', 'description']
	form_class = ItemForm
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(ItemUpdate, self).get_context_data(**kwargs)  # get the default context data
		itemId = self.kwargs['pk']
		text = SearchForm()
		rules = service.item_rules_string(itemId)
		user_name = self.request.user.username
		context['text'] = text
		context['user_name'] = user_name
		context['itemId'] = itemId
		context['pk'] = itemId
		context['rules'] = rules
		return context

	def get_object(self, queryset=None):
		item_details = service.get_item_details(item_id=self.kwargs['pk'])
		return Item.objects.create(
			name=item_details['name'],
			description=item_details['description'],
			category=item_details['category'],
			price=item_details['price'],
			quantity=item_details['quantity']
		)

	def form_valid(self, form):
		service.update_item(item_id = self.kwargs['pk'], item_dict =form.cleaned_data)
		return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class ItemDelete(DeleteView):
	model = Item
	# fields = ['name', 'owners', 'items', 'description']
	form_class = ItemForm
	template_name_suffix = '_delete_form'

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(ItemDelete, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		context['pk'] = self.object.id
		return context

	def get_object(self, queryset=None):
		item_details = service.get_item_details(item_id= self.kwargs['pk'])
		return Item.objects.create(
			name=item_details['name'],
			description=item_details['description'],
			category= item_details['category'],
			price= item_details['price'],
			quantity= item_details['quantity']
		)
	def delete(self, request, *args, **kwargs):
		service.delete_item(item_id = kwargs['pk'])
		return super(ItemDelete, self).delete(request, *args, **kwargs)


# def add_discount_to_item(request, pk):
# 	if request.method == 'POST':
# 		form = AddDiscountForm(request.POST)
# 		min_max_cond = MaxMinConditionForm(request.POST)
# 		if form.is_valid() and min_max_cond.is_valid():
# 			disc = form.save()
# 			if (min_max_cond.cleaned_data.get('cond_min_max')):
# 				cond_1 = min_max_cond.save()
# 				disc.conditions.add(cond_1)
# 				disc = form.save()
#
# 			item = Item.objects.get(id=pk)
# 			item.discounts.add(disc)
# 			item.save()
# 			percentageStr = form.cleaned_data.get('percentage')
# 			messages.success(request, 'add discount to item . percentage :  ' + str(percentageStr) + '%')
# 			return redirect('/store/home_page_owner/')
# 		messages.warning(request, 'error in :  ' + str(form.errors))
# 		return redirect('/store/home_page_owner/')
#
# 	else:
# 		context = {
# 			'text': SearchForm(),
# 			'pk': pk,
# 			'form': AddDiscountForm(),
# 			'cond_max_min': MaxMinConditionForm(),
# 		}
# 		return render(request, 'store/add_discount_to_item.html', context)

from .forms import DeleteOwners

@method_decorator(login_required, name='dispatch')
class StoreUpdate(UpdateView):
	model = Store
	# fields = ['name', 'owners', 'items', 'description']
	form_class = StoreForm
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(StoreUpdate, self).get_context_data(**kwargs)  # get the default context data
		text = SearchForm()
		rules = service.store_rules_string(store_id=self.kwargs['pk'])
		store_items = service.get_store_items(store_id=self.kwargs['pk'])

		store_managers = service.get_store_managers(store_id=self.kwargs['pk'])
		store_owners = service.get_store_owners(store_id=self.kwargs['pk'])
		del store_owners[0]
		all_managers = store_owners+store_managers
		# print(store_owners)
		delet_owners = DeleteOwners(all_managers,self.kwargs['pk'])


		user_name = self.request.user.username
		context['text'] = text
		context['user_name'] = user_name
		context['form_'] = UpdateItems(store_items)
		context['rules'] = rules
		context['delet_owners'] = delet_owners
		return context

	def get_object(self, queryset=None):
		store_details = service.get_store_details(store_id= self.kwargs['pk'])
		return Store.objects.create(
			name=store_details['name'],
			description=store_details['description']
		)

	def form_valid(self, form):
		service.update_store(store_id = self.kwargs['pk'], store_dict =form.cleaned_data)
		return super().form_valid(form)


@login_required
def change_store_owner_to_member(user_name_):
	owners_group = Group.objects.get(name="store_owners")
	user = User.objects.get(user_name=user_name_)
	owners_group.user_set.remove(user)


@method_decorator(login_required, name='dispatch')
class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	def delete(self, request, *args, **kwargs):
		store_id = kwargs['pk']
		if not service.can_remove_store(store_id=store_id, user_id=self.request.user.pk):
			messages.warning(request, 'there is no delete perm!')
			user_name = request.user.username
			text = SearchForm()
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})

		owner_name = service.get_store_creator(store_id = kwargs['pk'])
		ans = service.delete_store(store_id=kwargs['pk'])
		response = super(StoreDelete, self).delete(request, *args, **kwargs)
		messages.success(request, ans[1])
		if service.have_no_more_stores(owner_name=owner_name):
			user_name = request.user.username
			text = SearchForm()
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})
		else:
			return response

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(StoreDelete, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


from external_systems.money_collector.payment_system import Payment
from external_systems.supply_system.supply_system import Supply

from .forms import PayForm

pay_system = Payment()
supply_system = Supply()


#def get_discount_for_store(pk, amount, total):
# 	store_of_item = Store.objects.get(items__id__contains=pk)
# 	if not (len(store_of_item.discounts.all()) == 0):
# 		discount_ = store_of_item.discounts.all()[0]
# 		now = datetime.datetime.now().date()
# 		if (discount_.end_date >= now):
# 			conditions = discount_.conditions.all()
# 			if (len(conditions) > 0):
# 				for cond in conditions:
# 					if (amount <= cond.max_amount and amount >= cond.min_amount):
# 						percentage = discount_.percentage
# 						total = (100 - percentage) / 100 * float(total)
# 						str_ret = percentage
# 						return [str_ret, total]
# 			else:
# 				percentage = discount_.percentage
# 				total = (100 - percentage) / 100 * float(total)
# 				str_ret = percentage
# 				return [str_ret, total]
# 	else:
# 		return [0, total]
#
#
# def get_discount_for_item(pk, amount, total):
# 	item = Item.objects.get(id=pk)
# 	if not (len(item.discounts.all()) == 0):
# 		item_discount = item.discounts.all()[0]
# 		now = datetime.datetime.now().date()
# 		if (item_discount.end_date >= now):
# 			conditions_item = item_discount.conditions.all()
# 			if (len(conditions_item) > 0):
# 				for cond_i in conditions_item:
# 					if (amount <= cond_i.max_amount and amount >= cond_i.min_amount):
# 						percentage = item_discount.percentage
# 						total = (100 - percentage) / 100 * float(total)
# 						str_ret = percentage
# 						return [str_ret, total]
# 			else:
# 				percentage = item_discount.percentage
# 				total = (100 - percentage) / 100 * float(total)
# 				str_ret = percentage
# 				return [str_ret, total]
# 	else:
# 		return [0, total]
def get_store_of_item(item_id):
	return Store.objects.filter(items__id__contains=item_id)[0]




def buy_logic(item_id, amount, amount_in_db, user, shipping_details, card_details):
	transaction_id = -1
	supply_transaction_id = -1

	_item = Item.objects.get(id=item_id)

	messages_ = ''
	curr_item = Item.objects.get(id=item_id)
	if (amount <= amount_in_db):
		# print("good amount")
		total = amount * curr_item.price
		new_q = amount_in_db - amount
		total_after_discount = total
		# check item rules
		if check_item_rules(curr_item, amount, user) is False:
			# messages.warning(request, "you can't buy due to item policies")
			# return render(request, 'store/buy_item.html', context)
			messages_ = "you can't buy due to item policies"
			return False, 0, 0, messages_
		store_of_item = get_store_of_item(item_id)
		# check store rules
		if check_store_rules(store_of_item, amount, shipping_details['country'], user) is False:
			# messages.warning(request, "you can't buy due to store policies")
			messages_ = "you can't buy due to store policies"
			return False, 0, 0, messages_
		# check discounts
		# [precentage1, total_after_discount] = get_discount_for_store(item_id, amount, total)
		# [precentage2, total_after_discount] = get_discount_for_item(item_id, amount, total_after_discount)

		precentage1=0
		precentage2=0
		total_after_discount=0
		if precentage1 != 0:
			discount = str(precentage1)
			messages_ += '\n' + 'you have discount for store ' + discount
		if precentage2 != 0:
			discount = str(precentage2)
			messages_ += '\n' + 'you have discount for item ' + discount
		# try:
		# 	if pay_system.handshake():
		# 		print("pay hand shake")
		#
		# 		transaction_id = pay_system.pay(str(card_details.card_number), str(card_details.month), str(card_details.year), str(card_details.holder), str(card_details.ccv),
		# 		transaction_id = pay_system.pay(str(card_details.card_number), str(card_details.month),
		# 		                                str(card_details.year), str(card_details.holder), str(card_details.ccv),
		# 			# messages.warning(request, 'can`t pay !')
		# 			messages_ += '\n' + 'can`t pay !'
		# 			return False, 0, 0, messages_
		# 			# return redirect('/login_redirect')
		# 	else:
			# return redirect('/login_redirect')
		# 		messages_ += '\n' + 'can`t connect to pay system!'
		# 		return False, 0, 0, messages_
		# 		# return redirect('/login_redirect')
		#
			# return redirect('/login_redirect')
		# 		# print("supply hand shake")
		# 		supply_transaction_id = supply_system.supply(str(shipping_details.name), str(shipping_details.address), str(shipping_details.city), str(shipping_details.country),
		# 		                                             str(zip))
		# 		supply_transaction_id = supply_system.supply(str(shipping_details.name), str(shipping_details.address),
		# 		                                             str(shipping_details.city), str(shipping_details.country),
		# 			messages_ += '\n' +'can`t supply abort payment!'
		# 			return False, 0, 0, messages_
		# 			# messages.warning(request, 'can`t supply abort payment!')
		# 			messages_ += '\n' + 'can`t supply abort payment!'
		# 	else:
			# messages.warning(request, 'can`t supply abort payment!')
		# 		messages_ += '\n' +'can`t connect to supply system abort payment!'
		# 		return False, 0, 0, messages_
		# 		# messages.warning(request, 'can`t connect to supply system abort payment!')
		# 		# return redirect('/login_redirect')
		#
		# 	_item.quantity = amount_in_db - amount
		# 	_item.save()
		#
		# 	# store = get_item_store(_item.pk)
		# 	item_subject = ItemSubject(_item.pk)
		# 	try:
		# 		if (user.is_authenticated):
		# 			notification = Notification.objects.create(
		# 				msg=user.username + ' bought ' + str(amount) + ' pieces of ' + _item.name)
		# 			notification.save()
		# 			item_subject.subject_state = item_subject.subject_state + [notification.pk]
		# 		else:
		# 			notification = Notification.objects.create(
		# 				msg='A guest bought ' + str(amount) + ' pieces of ' + _item.name)
		# 			notification.save()
		# 			item_subject.subject_state = item_subject.subject_state + [notification.pk]
		# 	except Exception as e:
		# 		messages_ += 'cant connect websocket ' + str(e)
		#
		# 	_item_name = _item.name
		# 	# print("reached herre")
		# 	if (_item.quantity == 0):
		# 		_item.delete()
		#
		# 	messages_ += '\n'+ 'Thank you! you bought ' + _item_name +'\n'+'Total after discount: ' + str(total_after_discount) + ' $'+'\n'+'Total before: ' + str(total) + ' $'
		# 	#
		# 	# messages.success(request, 'Thank you! you bought ' + _item_name)
		# 	# messages.success(request, 'Total after discount: ' + str(total_after_discount) + ' $')
		# 	# messages.success(request, 'Total before: ' + str(total) + ' $')
		# 	# print("!!!!!!!!!!!!!!!!!!!!")
		# 	return redirect('/login_redirect')
		# except Exception as a:
		# 	print(a)
		# 	print(str(a))
		# 	traceback.print_exc()
		# 	if not (transaction_id == -1):
		# 		messages_ += '\n' +'failed and aborted pay! please try again!'
		# 		# messages.warning(request, 'failed and aborted pay! please try again!')
		# 		_item.quantity = amount_in_db
		# 		chech_cancle = pay_system.cancel_pay(transaction_id)
		# 		chech_cancle_supply = supply_system.cancel_supply(supply_transaction_id)
		# 	return redirect('/login_redirect')

		try:
			_item.quantity = amount_in_db - amount
			_item.save()

			# store = get_item_store(_item.pk)
			item_subject = ItemSubject(_item.pk)
			try:
				if (user.is_authenticated):
					notification = Notification.objects.create(
						msg=user.username + ' bought ' + str(amount) + ' pieces of ' + _item.name)
					notification.save()
					item_subject.subject_state = item_subject.subject_state + [notification.pk]
				else:
					notification = Notification.objects.create(
						msg='A guest bought ' + str(amount) + ' pieces of ' + _item.name)
					notification.save()
					item_subject.subject_state = item_subject.subject_state + [notification.pk]
			except Exception as e:
				messages_ += 'cant connect websocket ' + str(e)

			_item_name = _item.name
			# print("reached herre")
			if (_item.quantity == 0):
				_item.delete()

			messages_ += '\n' + 'Thank you! you bought ' + _item_name + '\n' + 'Total after discount: ' + str(
				total_after_discount) + ' $' + '\n' + 'Total before: ' + str(total) + ' $'
			return False, 0, 0, messages_
		except Exception as a:
			print(a)
			print(str(a))
			traceback.print_exc()
			if not (transaction_id == -1):
				messages_ += '\n' + 'failed and aborted pay! please try again!'
				# messages.warning(request, 'failed and aborted pay! please try again!')
				_item.quantity = amount_in_db
				chech_cancle = pay_system.cancel_pay(transaction_id)
				chech_cancle_supply = supply_system.cancel_supply(supply_transaction_id)
			return False, 0, 0, messages_

		messages_ = "you have discount for this item: " + discount + "%"
		return True, total, total_after_discount, messages_
	else:
		return False, 0, 0, messages_


def buy_item(request, pk):
	# return redirect('/store/contact/' + str(pk) + '/')
	print('heryyyyyyyyyyyy')
	form_class = BuyForm
	curr_item = Item.objects.get(id=pk)
	context = {
		'name': curr_item.name,
		'pk': curr_item.id,
		'form': form_class,
		'price': curr_item.price,
		'description': curr_item.description,
		'text': SearchForm(),
		'card': PayForm(),
		'shipping': ShippingForm(),
	}
	if request.method == 'POST':
		print("post")
		form = BuyForm(request.POST)
		shipping_form = ShippingForm(request.POST)
		supply_form = PayForm(request.POST)

		if form.is_valid() and shipping_form.is_valid() and supply_form.is_valid():
			# shipping
			country = shipping_form.cleaned_data.get('country')
			city = shipping_form.cleaned_data.get('city')
			zip = shipping_form.cleaned_data.get('zip')
			address = shipping_form.cleaned_data.get('address')
			name = shipping_form.cleaned_data.get('name')

			shipping_details = {'country': country, 'city': city, 'zip': zip, 'address': address, 'name': name}

			# card

			card_number = supply_form.cleaned_data.get('card_number')
			month = supply_form.cleaned_data.get('month')
			year = supply_form.cleaned_data.get('year')
			holder = supply_form.cleaned_data.get('holder')
			ccv = supply_form.cleaned_data.get('ccv')
			id = supply_form.cleaned_data.get('id')

			card_details = {'card_number': card_number, 'month': month, 'year': year, 'holder': holder, 'ccv': ccv,
			                'id': id}

			#########################buy proccss
			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			amount_in_db = _item.quantity

			valid, total, total_after_discount, messages_ = buy_logic(pk, amount, amount_in_db, request.user,
			                                                          shipping_details, card_details)
			if valid == False:
				messages.warning(request, messages_)
				return redirect('/login_redirect')
			else:
				messages.success(request, messages_)
				return redirect('/login_redirect')

		###########################end buy procces
		errors = str(form.errors) + str(shipping_form.errors) + str(supply_form.errors)
		messages.warning(request, 'error in :  ' + errors)
		return redirect('/login_redirect')
	else:
		form_class = BuyForm
		curr_item = Item.objects.get(id=pk)
		context = {
			'name': curr_item.name,
			'pk': curr_item.id,
			'form': form_class,
			'price': curr_item.price,
			'description': curr_item.description,
			'text': SearchForm(),
			'card': PayForm(),
			'shipping': ShippingForm(),
		}
		return render(request, 'store/buy_item.html', context)


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


def check_base_item_rule(rule_id, amount, user):
	rule = BaseItemRule.objects.get(id=rule_id)
	if rule.type == 'MAX' and amount > int(rule.parameter):
		return False
	elif rule.type == 'MIN' and amount < int(rule.parameter):
		return False
	return True


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


@login_required
def home_page_owner(request):
	text = SearchForm()
	user_name = request.user.username
	unread_ntfcs = NotificationUser.objects.filter(user=request.user.pk, been_read=False)
	context = {
		'user_name': user_name,
		'text': text,
		'owner_id': request.user.pk,
		'unread_notifications': len(unread_ntfcs)
	}
	return render(request, 'store/homepage_store_owner.html', context)


class AddItemToStore(CreateView):
	model = Item
	fields = ['name', 'description', 'price', 'quantity']


def itemAddedSucceffuly(request, store_id, id):
	x = 1
	return render(request, 'store/item_detail.html')


@permission_required_or_403('ADD_MANAGER', (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request, pk):
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			picked = form.cleaned_data.get('permissions')
			is_owner = form.cleaned_data.get('is_owner')
			[fail, message_] = service.add_manager(user_name, picked, is_owner, pk, request.user.username)
			if (fail):
				messages.warning(request, message_)
				return redirect('/store/home_page_owner/')
			messages.success(request, user_name + ' is appointed')
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')
	# do something with your results
	else:
		form = AddManagerForm
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'pk': pk,
			'form': form
		}

		return render(request, 'store/add_manager.html', context)


@permission_required_or_403('ADD_DISCOUNT', (Store, 'id', 'pk'))
@login_required
def add_discount_to_store(request,  pk, which_button):
	if request.method == 'POST':
		form = AddDiscountForm(pk, request.POST)
		if form.is_valid():
			#disc = form.save()
			# if (min_max_cond.cleaned_data.get('cond_min_max')):
			# cond_1 = min_max_cond.save()
			# disc.conditions.add(cond_1)
			# disc.save()
			# store = Store.objects.get(id=pk)
			# store.discounts.add(disc)
			# store.save()
			type = form.cleaned_data.get('type')
			condition = form.cleaned_data.get('condition')
			percentage = form.cleaned_data.get('percentage')
			amount = form.cleaned_data.get('amount')
			start_date = form.cleaned_data.get('start_date')
			end_date = form.cleaned_data.get('end_date')
			add_item = form.cleaned_data.get('add_item')
			item = form.cleaned_data.get('item')
			if condition is False and add_item is False:
				ans = service.add_discount(store_id=pk, percentage=percentage,  end_date=end_date)
			if condition is False and add_item is True:
				ans = service.add_discount(store_id=pk, percentage=percentage,  end_date=end_date, item=item)
			if condition is True and add_item is False:
				ans = service.add_discount(store_id=pk, kind=type, amount=amount, percentage=percentage, end_date=end_date)
			if condition is True and add_item is True:
				ans = service.add_discount(store_id=pk, kind=type, amount=amount, percentage=percentage, end_date=end_date, item=item)
			print(ans[1])
			messages.success(request, 'add discount :  ' + str(percentage) + '%')
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ' + str(form.errors))
		return redirect('/store/home_page_owner/')

	else:
		text = SearchForm()
		user_name = request.user.username
		discountForm = AddDiscountForm(pk)
		context = {
			'user_name': user_name,
			'text': text,
			'form': discountForm,
			'pk': pk,
		}
		return render(request, 'store/add_discount_to_store.html', context)


def owner_feed(request, owner_id):
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text,
		'owner_id_json': mark_safe(json.dumps(owner_id)),
		'owner_id': owner_id
	}
	return render(request, 'store/owner_feed.html', context)


def get_item_store(item_pk):
	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))
	# Might cause bug. Need to apply the item-in-one-store condition
	return stores[0]


from .models import BaseRule


def add_base_rule_to_store(request, pk, which_button):
	if request.method == 'POST':
		form = AddRuleToStore_base(request.POST)
		if form.is_valid():
			rule_id = -1
			# store = Store.objects.get(id=pk)
			rule = form.cleaned_data.get('rule')
			# operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			ans = service.add_base_rule_to_store(rule_type=rule, store_id=pk, parameter=parameter)
			if ans[0] == True:
				rule_id = ans[1]
				if which_button == 'ok':
					messages.success(request, 'added rule : ' + str(rule) + ' successfully!')
					return redirect('/store/home_page_owner/')
				if which_button == 'complex1':
					return redirect('/store/add_complex_rule_to_store_1/' + '_' + str(rule_id) + '/' + str(pk) + '/a')
				if which_button == 'complex2':
					return redirect('/store/add_complex_rule_to_store_2/' + '_' + str(rule_id) + '/' + str(pk) + '/a')
			else:
				messages.warning(request, ans[1])
				return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToStore_base()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'pk': pk,
			'which_button': which_button,
		}
		return render(request, 'store/add_base_rule_to_store.html', context)


def add_complex_rule_to_store_1(request, rule_id1, store_id, which_button):
	if request.method == 'POST':
		form = AddRuleToStore_withop(request.POST)
		if form.is_valid():
			rule_to_ret = -1
			store = Store.objects.get(id=store_id)
			rule = form.cleaned_data.get('rule')
			operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			ans = service.add_complex_rule_to_store_1(rule_type=rule, prev_rule=rule_id1, store_id=store_id,
			                                          operator=operator, parameter=parameter)
			if ans[0] == True:
				rule_to_ret = ans[1]
				if which_button == 'ok':
					messages.success(request, 'added rule successfully!')
					return redirect('/store/home_page_owner/')
				if which_button == 'complex1':
					return redirect(
						'/store/add_complex_rule_to_store_1/' + str(rule_to_ret) + '/' + str(store_id) + '/a')
				if which_button == 'complex2':
					return redirect(
						'/store/add_complex_rule_to_store_2/' + str(rule_to_ret) + '/' + str(store_id) + '/a')
			else:
				messages.warning(request, ans[1])
				return redirect('/store/home_page_owner/')
		# return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToStore_withop()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'store_id': store_id,
			'rule_id1': rule_id1,
			'which_button': which_button,
		}
		return render(request, 'store/add_complex_rule_to_store_1.html', context)


def add_complex_rule_to_store_2(request, rule_id_before, store_id, which_button):
	if request.method == 'POST':
		form = AddRuleToStore_two(request.POST)
		if form.is_valid():
			rule_to_ret = -1
			store = Store.objects.get(id=store_id)
			rule1 = form.cleaned_data.get('rule1')
			rule2 = form.cleaned_data.get('rule2')
			operator1 = form.cleaned_data.get('operator1')
			operator2 = form.cleaned_data.get('operator2')
			parameter1 = form.cleaned_data.get('parameter1')
			parameter2 = form.cleaned_data.get('parameter2')
			ans = service.add_complex_rule_to_store_2(rule1=rule1, parameter1=parameter1, rule2=rule2,
			                                          parameter2=parameter2, store_id=store_id, operator1=operator1,
			                                          operator2=operator2, prev_rule=rule_id_before)
			if ans[0] == True:
				if which_button == 'ok':
					messages.success(request, 'added rule successfully!')
					return redirect('/store/home_page_owner/')
				if which_button == 'complex1':
					return redirect('/store/add_complex_rule_to_store_2/' + str(ans[1]) + '/' + str(store_id) + '/a')
				if which_button == 'complex2':
					return redirect('/store/add_complex_rule_to_store_2/' + str(ans[1]) + '/' + str(store_id) + '/a')
			else:
				messages.warning(request, ans[1])
				return redirect('/store/home_page_owner/')
		# return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToStore_two()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'store_id': store_id,
			'rule_id_before': rule_id_before,
			'which_button': which_button,
		}
		return render(request, 'store/add_complex_rule_to_store_2.html', context)


from .models import BaseItemRule


def add_base_rule_to_item(request, pk, which_button):
	if request.method == 'POST':
		form = AddRuleToItem(request.POST)
		if form.is_valid():
			# rule_id = -1
			# item = Item.objects.get(id=pk)
			rule = form.cleaned_data.get('rule')
			parameter = form.cleaned_data.get('parameter')
			# brule = BaseItemRule(item=item, type=rule, parameter=parameter)
			# brule.save()
			# rule_id = brule.id
			ans = service.add_base_rule_to_item(item_id=pk, rule=rule, parameter=parameter)
			if which_button == 'ok':
				messages.success(request, 'added rule : ' + str(rule) + ' successfully!')
				return redirect('/store/home_page_owner/')
			if which_button == 'complex1':
				return redirect('/store/add_complex_rule_to_item_1/' + '_' + str(ans[1]) + '/' + str(pk) + '/a')
			if which_button == 'complex2':
				return redirect('/store/add_complex_rule_to_item_2/' + '_' + str(ans[1]) + '/' + str(pk) + '/a')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToItem()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'pk': pk,
			'which_button': which_button,
		}
		return render(request, 'store/add_base_rule_to_item.html', context)


def add_complex_rule_to_item_1(request, rule_id1, item_id, which_button):
	if request.method == 'POST':
		form = AddRuleToItem_withop(request.POST)
		if form.is_valid():
			rule_to_ret = -1
			item = Item.objects.get(id=item_id)
			rule = form.cleaned_data.get('rule')
			operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			ans = service.add_complex_rule_to_item_1(item_id=item_id, prev_rule=rule_id1, rule=rule, operator=operator,
			                                         parameter=parameter)
			if which_button == 'ok':
				messages.success(request, 'added rule successfully!')
				return redirect('/store/home_page_owner/')
			if which_button == 'complex1':
				return redirect('/store/add_complex_rule_to_item_1/' + str(ans[1]) + '/' + str(item_id) + '/a')
			if which_button == 'complex2':
				return redirect('/store/add_complex_rule_to_item_2/' + str(ans[1]) + '/' + str(item_id) + '/a')
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToItem_withop()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'item_id': item_id,
			'rule_id1': rule_id1,
			'which_button': which_button,
		}
		return render(request, 'store/add_complex_rule_to_item_1.html', context)


def add_complex_rule_to_item_2(request, rule_id_before, item_id, which_button):
	if request.method == 'POST':
		form = AddRuleToItem_two(request.POST)
		if form.is_valid():
			rule_to_ret = -1
			item = Item.objects.get(id=item_id)
			rule1 = form.cleaned_data.get('rule1')
			rule2 = form.cleaned_data.get('rule2')
			operator1 = form.cleaned_data.get('operator1')
			operator2 = form.cleaned_data.get('operator2')
			parameter1 = form.cleaned_data.get('parameter1')
			parameter2 = form.cleaned_data.get('parameter2')
			# baseRule1 = BaseItemRule(item=item, type=rule1, parameter=parameter1)
			# baseRule1.save()
			# rule_id1 = baseRule1.id
			# rule1_temp = '_' + str(rule_id1)
			# baseRule2 = BaseItemRule(item=item, type=rule2, parameter=parameter2)
			# baseRule2.save()
			# rule_id2 = baseRule2.id
			# rule2_temp = '_' + str(rule_id2)
			# cr = ComplexItemRule(left=rule1_temp, right=rule2_temp, operator=operator1, item=item)
			# cr.save()
			# cr_id = cr.id
			# cr2 = ComplexItemRule(left=rule_id_before, right=cr_id, operator=operator2, item=item)
			# cr2.save()
			# cr_id2 = cr2.id
			ans = service.add_complex_rule_to_item_2(item_id=item_id, prev_rule=rule_id_before, rule1=rule1,
			                                         parameter1=parameter1, rule2=rule2, parameter2=parameter2,
			                                         operator1=operator1, operator2=operator2)
			if which_button == 'ok':
				messages.success(request, 'added rule successfully!')
				return redirect('/store/home_page_owner/')
			if which_button == 'complex1':
				return redirect('/store/add_complex_rule_to_item_2/' + str(ans[1]) + '/' + str(item_id) + '/a')
			if which_button == 'complex2':
				return redirect('/store/add_complex_rule_to_item_2/' + str(ans[1]) + '/' + str(item_id) + '/a')
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')
	else:
		ruleForm = AddRuleToItem_two()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'item_id': item_id,
			'rule_id_before': rule_id_before,
			'which_button': which_button,
		}
		return render(request, 'store/add_complex_rule_to_item_2.html', context)


def remove_rule_from_store(request, pk, type, store):
	if type == 2:
		complexRule = ComplexStoreRule.objects.get(id=pk)
		delete_complex(complexRule.id)
	else:
		baseRule = BaseRule.objects.get(id=pk)
		delete_base(baseRule.id)
	messages.success(request, 'remove rule successfully!')
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text,
	}
	return redirect('/store/update/' + str(store))


def delete_complex(rule_id):
	rule = ComplexStoreRule.objects.get(id=rule_id)
	if rule.left[0] == '_':
		BaseRule.objects.get(id=int(rule.left[1:])).delete()
	else:
		delete_complex(int(rule.left))
	if rule.right[0] == '_':
		BaseRule.objects.get(id=int(rule.right[1:])).delete()
	else:
		delete_complex(int(rule.right))
	rule.delete()


def delete_base(rule_id):
	rule = BaseRule.objects.get(id=rule_id)
	rule.delete()


def remove_rule_from_item(request, pk, type, item):
	if type == 2:
		complexRule = ComplexItemRule.objects.get(id=pk)
		delete_complex_item(complexRule.id)
	else:
		baseRule = BaseItemRule.objects.get(id=pk)
		delete_base_item(baseRule.id)
	messages.success(request, 'remove rule successfully!')
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text,
	}
	return redirect('/store/update_item/' + str(item))


def delete_complex_item(rule_id):
	rule = ComplexItemRule.objects.get(id=rule_id)
	if rule.left[0] == '_':
		BaseItemRule.objects.get(id=int(rule.left[1:])).delete()
	else:
		delete_complex_item(int(rule.left))
	if rule.right[0] == '_':
		BaseItemRule.objects.get(id=int(rule.right[1:])).delete()
	else:
		delete_complex_item(int(rule.right))
	rule.delete()


def delete_base_item(rule_id):
	rule = BaseItemRule.objects.get(id=rule_id)
	rule.delete()


class NotificationsListView(ListView):
	model = Notification
	template_name = 'store/owner_feed.html'

	def get_queryset(self):
		return service.get_user_notifications(user_id = self.request.user.pk)

	def get_context_data(self, **kwargs):
		context = super(NotificationsListView, self).get_context_data(**kwargs)  # get the default context data
		context['owner_id'] = self.request.user.pk
		context['unread_notifications'] = 0
		service.mark_notification_read(user_id = self.request.user.pk)
		return context



def delete_owner(request,pk_owner,pk_store):
	if (service.remove_manager_from_store(pk_store,pk_owner)):
		messages.success(request, 'delete owner')  # <-
		return redirect('/store/home_page_owner/')
	else:
		messages.warning(request, 'can`t delete owner')  # <-
		return redirect('/store/home_page_owner/')


