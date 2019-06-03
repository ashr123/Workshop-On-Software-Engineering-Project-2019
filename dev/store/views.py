import json

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
from guardian.shortcuts import assign_perm
from websocket import create_connection

from trading_system.forms import SearchForm
from . import forms
from .forms import BuyForm, AddManagerForm, AddDiscountToStore, AddRuleToStore, AddRuleToItem
from .forms import ShippingForm
from .models import Item
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


@permission_required_or_403('ADD_ITEM',
                            (Store, 'id', 'pk'))
@login_required
def add_item(request, pk):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			item = form.save()
			curr_store = Store.objects.get(id=pk)
			curr_store.items.add(item)
			messages.success(request, 'Your Item was added successfully!')  # <-
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
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             description=open_store_form.cleaned_data.get('description'))
		store.owners.add(request.user)
		store.save()
		_user = request.user
		messages.success(request, 'Your Store was added successfully!')  # <-
		my_group = Group.objects.get_or_create(name="store_owners")
		my_group = Group.objects.get(name="store_owners")
		_user.groups.add(my_group)
		assign_perm('ADD_ITEM', _user, store)
		assign_perm('REMOVE_ITEM', _user, store)
		assign_perm('EDIT_ITEM', _user, store)
		assign_perm('ADD_MANAGER', _user, store)
		assign_perm('REMOVE_STORE', _user, store)
		assign_perm('ADD_DISCOUNT', _user, store)
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
		context = super(StoreDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		context['user_name'] = user_name
		return context


# def get_queryset(self):
# 	return Store.objects.get(id=self.kwargs['pk']).items.all()


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		context['user_name'] = self.request.user.username
		return context

	def get_queryset(self):
		# return Store.objects.filter(owner_id=self.request.user.id)
		return Store.objects.filter(owners__id__in=[self.request.user.id])


class ItemListView(ListView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		context['user_name'] = self.request.user.username
		return context

	def get_queryset(self, **kwargs):
		store = Store.objects.get(id=kwargs['store_pk'])
		items = store.items.all()


# return Item.objects.filter(owners__id__in=[self.request.user.id])


class ItemDetailView(DetailView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(ItemDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


from .forms import UpdateItems, StoreForm, ItemForm


@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):
	model = Item
	# fields = ['name', 'owners', 'items', 'description']
	form_class = ItemForm
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		itemId = self.kwargs['pk']
		text = SearchForm()
		user_name = self.request.user.username
		context = super(ItemUpdate, self).get_context_data(**kwargs)
		context['text'] = text
		context['user_name'] = user_name
		context['itemId'] = itemId
		return context


@method_decorator(login_required, name='dispatch')
class StoreUpdate(UpdateView):
	model = Store
	# fields = ['name', 'owners', 'items', 'description']
	form_class = StoreForm
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		# if not (self.request.user.has_perm('EDIT_ITEM')):
		# 	user_name = self.request.user.username
		# 	text = SearchForm()
		# 	messages.warning(self.request, 'there is no edit perm!')
		# 	return render(self.request, 'homepage_member.html', {'text': text, 'user_name': user_name})
		text = SearchForm()
		store = Store.objects.get(id=self.object.id)
		store_rules = BaseRule.objects.all().filter(store=store)
		store_items = store.items.all()
		user_name = self.request.user.username
		context = super(StoreUpdate, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		context['user_name'] = user_name
		context['form_'] = UpdateItems(store_items)
		context['rules'] = store_rules
		return context


# def update(self, request, *args, **kwargs):
# 	if not (self.request.user.has_perm('EDIT_ITEM')):
# 		messages.warning(request, 'there is no edit perm!')
# 		user_name = request.user.username
# 		text = SearchForm()
# 		return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})
# 	return super().update(request, *args, **kwargs)


def have_no_more_stores(user_pk):
	tmp = Store.objects.filter(owners__username__contains=user_pk)
	return len(tmp) == 0


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
		store = Store.objects.get(id=kwargs['pk'])
		items_to_delete = store.items.all()
		# print('\n h    hhhhhhh', items_to_delete)
		if not (self.request.user.has_perm('REMOVE_STORE', store)):
			messages.warning(request, 'there is no delete perm!')
			user_name = request.user.username
			text = SearchForm()
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})

		owner_name = store.owners.all()[0]  # craetor

		# print('\n id : ', owner_name)
		for item_ in items_to_delete:
			# print('\n delete ')
			item_.delete()

		response = super(StoreDelete, self).delete(request, *args, **kwargs)

		messages.success(request, 'store was deleted : ', store.name)
		if have_no_more_stores(owner_name):

			owners_group = Group.objects.get(name="store_owners")
			user = User.objects.get(username=owner_name)
			owners_group.user_set.remove(user)

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

from .forms import PayForm

# FORMS_ = [('_step1', BuyForm),
#           ('_step2', PayForm),
#
#           ]
# TEMPLATES_ = {'_step1': 'store/buy_step_1.html',
#               '_step2': 'store/buy_step_2.html',
#               }
#
# class ContactWizard(SessionWizardView):
# 	def get_context_data(self, form, **kwargs):
# 		context = super(ContactWizard, self).get_context_data(form=form, **kwargs)
# 		if self.steps.current == '_step1':
# 			pk = self.kwargs['pk']
# 			text = SearchForm()
# 			form_class = BuyForm
# 			curr_item = Item.objects.get(id=pk)
# 			context.update({
# 				'name': curr_item.name,
# 				'pk': curr_item.id,
# 				'form': form_class,
# 				'price': curr_item.price,
# 				'description': curr_item.description,
# 				'text': text
# 			})
# 		if self.steps.current == '_step2':
# 			if self.request.user.is_authenticated:
# 				if "store_owners" in self.request.user.groups.values_list('name',
# 				                                                          flat=True) or "store_managers" in self.request.user.groups.values_list(
# 					'name', flat=True):
# 					base_template_name = 'store/homepage_store_owner.html'
# 				else:
# 					base_template_name = 'homepage_member.html'
# 			else:
# 				base_template_name = 'homepage_guest.html'
#
# 			pay_form = PayForm()
# 			context.update({
# 				'base_template_name': base_template_name,
# 				'text': SearchForm(),
# 				'formset': pay_form,
# 			})
# 		return context
#
# 	def get_template_names(self):
# 		return [TEMPLATES_[self.steps.current]]
#
# 	def done(self, form_list, **kwargs):
# 		return redirect('/login_redirect')

pay_system = Payment()


def buy_item(request, pk):
	# return redirect('/store/contact/' + str(pk) + '/')
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
		form = BuyForm(request.POST)
		shipping_form = ShippingForm(request.POST)
		supply_form = PayForm(request.POST)

		if form.is_valid() and shipping_form.is_valid() and supply_form.is_valid():
			# transaction_id = 0
			# if pay_system.handshake():
			# 	if request.user.is_authenticated:
			# 		if "store_owners" in request.user.groups.values_list('name',
			# 		                                                     flat=True) or "store_managers" in request.user.groups.values_list(
			# 			'name', flat=True):
			# 			base_template_name = 'store/homepage_store_owner.html'
			# 		else:
			# 			base_template_name = 'homepage_member.html'
			# 	else:
			# 		base_template_name = 'homepage_guest.html'
			#
			# 	pay_form = PayForm()
			# 	context = {
			# 		'base_template_name': base_template_name,
			# 		'text': SearchForm(),
			# 		'form': pay_form,
			# 	}
			#
			# 	transaction_id = pay_system.pay('2222333344445555', '4', '2021', 'Israel Israelovice', '262',
			# 	                                '20444444')
			# else:
			# 	messages.warning(request, 'can`t connect to pay system!')
			# 	return redirect('/login_redirect')

			# shipping
			country = shipping_form.cleaned_data.get('country')
			city = shipping_form.cleaned_data.get('city')
			zip = shipping_form.cleaned_data.get('zip')
			address = shipping_form.cleaned_data.get('address')
			name = shipping_form.cleaned_data.get('name')

			# card
			card_number = supply_form.cleaned_data.get('card_number')
			month = supply_form.cleaned_data.get('month')
			year = supply_form.cleaned_data.get('year')
			holder = supply_form.cleaned_data.get('holder')
			ccv = supply_form.cleaned_data.get('ccv')
			id = supply_form.cleaned_data.get('id')

			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			amount_in_db = _item.quantity
			if (amount <= amount_in_db):
				total = amount * _item.price
				new_q = amount_in_db - amount

				store_of_item = Store.objects.get(items__id__contains=pk)
				storeRules = BaseRule.objects.all().filter(store=store_of_item)
				for rule in storeRules:
					if rule.type == 'MAX' and amount > int(rule.parameter):
						messages.warning(request, "you can only buy maximum " + rule.parameter)
						return render(request, 'store/buy_item.html', context)
					elif rule.type == 'MIN' and amount < int(rule.parameter):
						messages.warning(request, "you can only buy minimum " + rule.parameter)
						return render(request, 'store/buy_item.html', context)
					elif rule.type == 'FOR' and country is rule.parameter:
						messages.warning(request, "sorry we cant deliver to " + rule.parameter)
						return render(request, 'store/buy_item.html', context)
					elif rule.type == 'REG' and not request.user.is_authenticated:
						messages.warning(request, "sorry only members can purchase")
						return render(request, 'store/buy_item.html', context)

					itemRules = ItemRule.objects.all().filter(item=_item)
					for item_rule in itemRules:
						if item_rule.type == 'MAX' and amount > int(item_rule.parameter):
							messages.warning(request, "you can only buy maximum " + item_rule.parameter + " of this item")
							return render(request, 'store/buy_item.html', context)
						elif item_rule.type == 'MIN' and amount < int(item_rule.parameter):
							messages.warning(request, "you can only buy minimum " + item_rule.parameter + " of this item")
							return render(request, 'store/buy_item.html', context)
				_item.quantity = new_q
				_item.save()
				if (store_of_item.discount > 0):
					total = (100 - store_of_item.discount) / 100 * float(total)
					messages.success(request,
					                 'you have discount for this store : ' + str(store_of_item.discount) + ' %')  # <-
				# messages.success(request, 'YES! at the moment you bought  : ' + _item.description)  # <-
				# messages.success(request, 'total : ' + str(total) + ' $')  # <-

				store = get_item_store(_item.pk)
				for owner in store.owners.all():
					try:
						ws = create_connection("ws://127.0.0.1:8000/ws/store_owner_feed/{}/".format(owner.id))
						if (request.user.is_authenticated):
							ws.send(
								json.dumps({'message': 'user : ' + request.user.username + ' BOUGHT AN ITEM FROM YOU'}))
						else:
							ws.send(json.dumps({'message': 'Guest BOUGHT AN ITEM FROM YOU'}))
					except:
						messages.warning(request, 'cant connect owner')
				_item_name = _item.name
				if (_item.quantity == 0):
					_item.delete()
				messages.success(request, 'Thank you! you bought ' + _item_name)  # <-
				# messages.success(request, 'transaction id:  ' + str(transaction_id))  # <-
				messages.success(request, 'Total : ' + str(total) + ' $')  # <-
				return redirect('/login_redirect')
			messages.warning(request, 'there is no such amount ! please try again!')
			return redirect('/login_redirect')
		messages.warning(request, 'error in :  ', form.errors)
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


@login_required
def home_page_owner(request):
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text,
		'owner_id': request.user.pk,
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
			try:
				user_ = User.objects.get(username=user_name)
			except:
				messages.warning(request, 'no such user')
				return redirect('/store/add_manager_to_store/' + str(pk) + '/')
			store_ = Store.objects.get(id=pk)
			if user_name == request.user.username:
				messages.warning(request, 'can`t add yourself as a manager!')
				return redirect('/store/home_page_owner/')
			pre_store_owners = store_.owners.all()
			# print('\n owners: ' ,pre_store_owners)
			for owner in pre_store_owners:
				if (owner.username == user_name):
					messages.warning(request, 'allready owner')
					return redirect('/store/home_page_owner/')

			if (user_ == None):
				messages.warning(request, 'No such user')
				return redirect('/store/home_page_owner/')
			for perm in picked:
				assign_perm(perm, user_, store_)
			if (is_owner):
				store_owners_group = Group.objects.get(name="store_owners")
				user_.groups.add(store_owners_group)
				store_.owners.add(user_)
			else:
				store_managers = Group.objects.get_or_create(name="store_managers")
				store_managers = Group.objects.get(name="store_managers")
				user_.groups.add(store_managers)

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
def add_discount_to_store(request, pk):
	if request.method == 'POST':
		form = AddDiscountToStore(request.POST)
		if form.is_valid():
			discount = form.cleaned_data.get('discount')
			store = Store.objects.get(id=pk)
			store.discount = discount
			store.save()
			messages.success(request, 'add discount :  ' + str(discount) + '%')
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')

	else:
		text = SearchForm()
		user_name = request.user.username
		discountForm = AddDiscountToStore()
		context = {
			'user_name': user_name,
			'text': text,
			'form': discountForm,
			'pk': pk,
		}
		return render(request, 'store/add_discount_to_store.html', context)


# def update_item(request, pk):
# 	if request.method == "POST":
#
# 		form = ItemForm(request.POST or None)
#
# 		if form.is_valid():
# 			obj = form.save(commit=False)
#
# 			obj.save()
#
# 			messages.success(request, "You successfully updated the post")
#
# 			return redirect(request.META.get('HTTP_REFERER', '/'))
#
# 		else:
# 			return render(request, 'store/edit_item.html', {'form': form,
# 			                                                'error': 'The form was not updated successfully. Please enter in a title and content'})
# 	else:
# 		return render(request, 'store/edit_item.html', {
# 			'store': pk,
# 			'form': ItemForm,
# 			'store_name': Store.objects.get(id=pk).name,  # TODO
# 			'user_name': request.user.username,
# 			'text': SearchForm(),
# 		})
#

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


def add_rule_to_store(request, pk):
	if request.method == 'POST':
		form = AddRuleToStore(request.POST)
		if form.is_valid():
			store = Store.objects.get(id=pk)
			rule = form.cleaned_data.get('rules')
			# operator = form.cleaned_data.get('operator')
			parameter = form.cleaned_data.get('parameter')
			if rule == 'MAX_QUANTITY' or rule == 'MIN_QUANTITY':
				try:
					int(parameter)
					if int(parameter) > 0:
						BaseRule(store=store, type=rule, parameter=parameter).save()
						messages.success(request, 'added rule :  ' + str(rule) + ' successfully!')
				except ValueError:
					messages.warning(request, 'Enter a number please')
			else:
				BaseRule(store=store, type=rule, parameter=parameter).save()
				messages.success(request, 'added rule :  ' + str(rule) + 'successfully!')
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, form.errors)
			return redirect('/store/home_page_owner/')

	else:
		ruleForm = AddRuleToStore()
		text = SearchForm()
		user_name = request.user.username
		context = {
			'user_name': user_name,
			'text': text,
			'form': ruleForm,
			'pk': pk,
		}
		return render(request, 'store/add_rule_to_store.html', context)

from .models import ItemRule
def add_rule_to_item(request, pk):
		if request.method == 'POST':
			form = AddRuleToStore(request.POST)
			if form.is_valid():
				item = Item.objects.get(id=pk)
				rule = form.cleaned_data.get('rules')
				# operator = form.cleaned_data.get('operator')
				parameter = form.cleaned_data.get('parameter')
				ItemRule(item=item, type=rule, parameter=parameter).save()
				messages.success(request, 'added rule :  ' + str(rule) + ' successfully!')
				return redirect('/store/home_page_owner/')
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
			}
			return render(request, 'store/add_rule_to_item.html', context)


def remove_rule_from_store(request, pk):
	BaseRule.objects.get(id=pk).delete()
	messages.success(request, 'removed rule successfully!')
