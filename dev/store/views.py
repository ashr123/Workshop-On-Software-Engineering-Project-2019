import decimal
from datetime import date
import json
import traceback
import logging
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
from . import forms
from .forms import BuyForm, AddManagerForm, AddRuleToItem, AddRuleToStore_base, AddRuleToStore_withop, \
	AddRuleToStore_two, AddDiscountForm, AddComplexDiscountForm
from .forms import ShippingForm, AddRuleToItem_withop, AddRuleToItem_two
from .models import Item, ComplexStoreRule, ComplexItemRule, Discount, ComplexDiscount
from .models import Store

log_setup = logging.getLogger('event log')
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fileHandler = logging.FileHandler('event.log', mode='a')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log_setup.setLevel(logging.INFO)
log_setup.addHandler(fileHandler)
log_setup.addHandler(streamHandler)
log_setup1 = logging.getLogger('error log')
fileHandler1 = logging.FileHandler('error.log', mode='a')
fileHandler1.setFormatter(formatter)
streamHandler1 = logging.StreamHandler()
streamHandler1.setFormatter(formatter)
log_setup1.setLevel(logging.ERROR)
log_setup1.addHandler(fileHandler1)
log_setup1.addHandler(streamHandler1)
logev = logging.getLogger('event log')
loger = logging.getLogger('error log')


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
		logev.info('add_item post')
		form = ItemForm(request.POST)
		if form.is_valid():
			ans = service.add_item_to_store(item_json=s_json.dumps(form.cleaned_data),
			                                store_id=pk, user_id=request.user.pk)
			messages.success(request, ans[1])  # <-
			logev.info('add_item post s')
			return redirect('/store/home_page_owner/')
		else:
			loger.warning('add_item fail not a valid form')
			messages.warning(request, 'Problem with filed : ', form.errors, 'please try again!')  # <-
			return redirect('/store/home_page_owner/')
	else:
		logev.info('add_item get')
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
		messages.success(request, "your new store added successfully")
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
		return Store.objects.filter(managers__id__in=[self.request.user.id]) | Store.objects.filter(
			owners__id__in=[self.request.user.id])


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
		service.update_item(item_id=self.kwargs['pk'], item_dict=form.cleaned_data, user_id=self.request.user.pk)
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
		item_details = service.get_item_details(item_id=self.kwargs['pk'])
		return Item.objects.create(name=item_details['name'],
		                           description=item_details['description'],
		                           category=item_details['category'],
		                           price=item_details['price'],
		                           quantity=item_details['quantity'])


	def delete(self, request, *args, **kwargs):
		service.delete_item(item_id=kwargs['pk'], user_id=request.user.pk)
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
		all_managers = store_owners + store_managers
		# print(store_owners)
		context['text'] = text
		context['user_name'] = self.request.user.username
		context['form_'] = UpdateItems(store_items)
		context['rules'] = rules
		context['delete_owners'] = DeleteOwners(all_managers, self.kwargs['pk'])
		return context

	def get_object(self, queryset=None):
		store_details = service.get_store_details(store_id=self.kwargs['pk'])
		return Store.objects.create(
			name=store_details['name'],
			description=store_details['description']
		)

	def form_valid(self, form):
		service.update_store(store_id=self.kwargs['pk'], store_dict=form.cleaned_data)
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

		owner_name = service.get_store_creator(store_id=kwargs['pk'])
		ans = service.delete_store(store_id=kwargs['pk'], user_id=request.user.pk)
		# response = super(StoreDelete, self).delete(request, *args, **kwargs)
		messages.success(request, ans[1])
		if service.have_no_more_stores((User.objects.get(username=owner_name)).id):
			user_name = request.user.username
			text = SearchForm()
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})
		else:
			return redirect('/login_redirect')

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


# def get_discount_for_store(pk, amount, total):
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


def buy_item(request, pk):
	if request.method == 'POST':
		print("post")
		form = BuyForm(request.POST)
		shipping_form = ShippingForm(request.POST)
		supply_form = PayForm(request.POST)

		if form.is_valid() and shipping_form.is_valid() and supply_form.is_valid():
			# shipping
			country = shipping_form.cleaned_data.get('country')
			city = shipping_form.cleaned_data.get('city')
			zip1 = shipping_form.cleaned_data.get('zip1')
			address = shipping_form.cleaned_data.get('address')
			name = shipping_form.cleaned_data.get('name')

			shipping_details = {'country': country, 'city': city, 'zip1': zip1, 'address': address, 'name': name}

			# card

			card_number = supply_form.cleaned_data.get('card_number')
			month = supply_form.cleaned_data.get('month')
			year = supply_form.cleaned_data.get('year')
			holder = supply_form.cleaned_data.get('holder')
			cvc = supply_form.cleaned_data.get('cvc')
			id1 = supply_form.cleaned_data.get('id1')

			card_details = {'card_number': card_number, 'month': month, 'year': year, 'holder': holder, 'cvc': cvc,
			                'id1': id1}

			#########################buy proccss
			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			amount_in_db = _item.quantity

			valid, total, total_after_discount, messages_ = service.buy_logic(pk, amount, amount_in_db, request.user,shipping_details, card_details)

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


from .forms import ApproveForm
from trading_system.views import get_all_whait_agreement_t_need_to_approve
@login_required
def home_page_owner(request):
	text = SearchForm()
	user_name = request.user.username
	unread_ntfcs = NotificationUser.objects.filter(user=request.user.pk, been_read=False)
	approve_list = get_all_whait_agreement_t_need_to_approve(request.user)
	approved_user_per_store ={}
	for a in approve_list:
		approved_user_per_store[a.user_to_wait.id] = a.store.id

	approve_form = ApproveForm(approved_user_per_store)
	print('--------------------------------------------------',approved_user_per_store)
	context = {
		'user_name': user_name,
		'text': text,
		'owner_id': request.user.pk,
		'unread_notifications': len(unread_ntfcs),
		'approve_form':approve_form,
	}
	return render(request, 'store/homepage_store_owner.html', context)


class AddItemToStore(CreateView):
	model = Item
	fields = ['name', 'description', 'price', 'quantity']


def itemAddedSucceffuly(request, store_id, id1):
	return render(request, 'store/item_detail.html')


# @transaction.atomic
@permission_required_or_403('ADD_MANAGER', (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request, pk):
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			picked = form.cleaned_data.get('permissions')
			is_owner = form.cleaned_data.get('is_owner')
			is_partner = form.cleaned_data.get('is_partner')
			[fail, message_] = service.add_manager(user_name, picked, is_owner, pk, request.user.username,is_partner)
			if fail:
				messages.warning(request, message_)
				return redirect('/store/home_page_owner/')
			messages.success(request, user_name + ' is appointed' + message_)
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
def add_discount_to_store(request, pk, which_button):
	if request.method == 'POST':
		form = AddDiscountForm(pk, request.POST)
		if form.is_valid():
			type = form.cleaned_data.get('type')
			percentage = form.cleaned_data.get('percentage')
			amount = form.cleaned_data.get('amount')
			end_date = form.cleaned_data.get('end_date')
			item = form.cleaned_data.get('item')
			ans = service.add_discount(store_id=pk, type=type, amount=amount, percentage=percentage, end_date=end_date,
			                           item_id=item.pk)
			if which_button == 'ok':
				ans = service.add_discount(store_id=pk, type=type, amount=amount, percentage=percentage,
				                           end_date=end_date, item_id=item.pk)
				messages.success(request, 'add discount :  ' + str(percentage) + '%')
				return redirect('/store/home_page_owner/')
			if which_button == 'complex':
				return redirect('/store/add_complex_discount_to_store/' + str(pk) + '/' + '_' + str(ans[1]) + '/a')

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


@permission_required_or_403('ADD_DISCOUNT', (Store, 'id', 'pk'))
@login_required
def add_complex_discount_to_store(request, pk, disc, which_button):
	if request.method == 'POST':
		form = AddComplexDiscountForm(pk, request.POST)
		if form.is_valid():
			operator = form.cleaned_data.get('operator')
			type = form.cleaned_data.get('type')
			percentage = form.cleaned_data.get('percentage')
			amount = form.cleaned_data.get('amount')
			end_date = form.cleaned_data.get('end_date')
			item = form.cleaned_data.get('item')
			if(item is None):
				ans = service.add_discount(store_id=pk, type=type, amount=amount, percentage=percentage, end_date=end_date,
			                           item_id=None)
			else:
				ans = service.add_discount(store_id=pk, type=type, amount=amount, percentage=percentage,
				                           end_date=end_date,
				                           item_id=item.pk)
			complex = service.add_complex_discount(store_id=pk, left='_' + str(ans[1]), right=disc, operator=operator)
			if which_button == 'ok':
				messages.success(request, 'add complex discount successfully')
				return redirect('/store/home_page_owner/')
			if which_button == 'complex':
				return redirect('/store/add_complex_discount_to_store/' + str(pk) + '/' + str(complex[1]) + '/a')
		messages.warning(request, 'error in :  ' + str(form.errors))
		return redirect('/store/home_page_owner/')
	else:
		text = SearchForm()
		user_name = request.user.username
		discountForm = AddComplexDiscountForm(pk)
		context = {
			'user_name': user_name,
			'text': text,
			'form': discountForm,
			'pk': pk,
		}
		return render(request, 'store/add_complex_discount_to_store.html', context)


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
			ans = service.add_base_rule_to_store(rule_type=rule, store_id=pk, parameter=parameter,
			                                     user_id=request.user.pk)
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
			rule = form.cleaned_data.get('rule')
			operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			ans = service.add_complex_rule_to_store_1(rule_type=rule, prev_rule=rule_id1, store_id=store_id,
			                                          operator=operator, parameter=parameter, user_id=request.user.pk)
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
			rule1 = form.cleaned_data.get('rule1')
			rule2 = form.cleaned_data.get('rule2')
			operator1 = form.cleaned_data.get('operator1')
			operator2 = form.cleaned_data.get('operator2')
			parameter1 = form.cleaned_data.get('parameter1')
			parameter2 = form.cleaned_data.get('parameter2')
			ans = service.add_complex_rule_to_store_2(rule1=rule1, parameter1=parameter1, rule2=rule2,
			                                          parameter2=parameter2, store_id=store_id, operator1=operator1,
			                                          operator2=operator2, prev_rule=rule_id_before, user_id=request.user.pk)
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
			ans = service.add_base_rule_to_item(item_id=pk, rule=rule, parameter=parameter, user_id=request.user.pk)
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
			rule = form.cleaned_data.get('rule')
			operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			ans = service.add_complex_rule_to_item_1(item_id=item_id, prev_rule=rule_id1, rule=rule, operator=operator,
			                                         parameter=parameter, user_id=request.user.pk)
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
			                                         operator1=operator1, operator2=operator2,
			                                         user_id=request.user.pk)
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


def remove_rule_from_store(request, pk, type1, store):
	if type1 == 2:
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


def remove_rule_from_item(request, pk, type1, item):
	if type1 == 2:
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
		return service.get_user_notifications(user_id=self.request.user.pk)

	def get_context_data(self, **kwargs):
		context = super(NotificationsListView, self).get_context_data(**kwargs)  # get the default context data
		context['owner_id'] = self.request.user.pk
		context['unread_notifications'] = 0
		service.mark_notification_read(user_id=self.request.user.pk)
		return context


def delete_owner(request, pk_owner, pk_store):
	print('remove omanager: ',pk_owner)
	if (service.remove_manager_from_store(pk_store, pk_owner)):
		messages.success(request, 'delete owner')  # <-
		return redirect('/store/home_page_owner/')
	else:
		messages.warning(request, 'can`t delete owner')  # <-
		return redirect('/store/home_page_owner/')
