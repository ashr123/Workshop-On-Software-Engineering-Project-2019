from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, redirect, render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm

from trading_system.forms import SearchForm
from . import forms
from .forms import ItemForm, BuyForm, AddManagerForm
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
			messages.warning(request, 'Problem with filed : !', form.errors, 'please try again!')  # <-
			return redirect('/store/home_page_owner/')
	else:
		form_class = ItemForm
		curr_store = Store.objects.get(id=pk)
		store_name = curr_store.name
		context = {
			'store': pk,
			'form': form_class,
			'store_name': store_name
		}
		print('\ndebug\n\n', pk)
		return render(request, 'store/add_item.html', context)


@login_required
def add_store(request):
	# g = GeoIP2()
	# print('\n\ncountry :  ',get_country_of_request(request))
	# print('\n\ncountry :  ', g.country('132.73.202.157'))
	user_groups = request.user.groups.values_list('name', flat=True)
	if "store_owners" in user_groups:
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
		context = super(StoreDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(StoreListView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context

	def get_queryset(self):
		# return Store.objects.filter(owner_id=self.request.user.id)
		cur_user_id = self.request.user.id
		return Store.objects.filter(owners__id__in=[cur_user_id])


class ItemListView(ListView):
	model = Item
	paginate_by = 100  # if pagination is desired


class ItemDetailView(DetailView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(ItemDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


@method_decorator(login_required, name='dispatch')
class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owners', 'items', 'description']
	template_name_suffix = '_update_form'
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(StoreUpdate, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


# def update(self, request, *args, **kwargs):
# 	store = Store.objects.get(id=kwargs['pk'])
# 	owner_id = store.owner_id
# 	response = super(StoreUpdate, self).update(request, *args, **kwargs)
# 	user_name = request.user.username
# 	text = SearchForm()
# 	context['text'] = text
# 	return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})
#


def have_no_more_stores(user_pk):
	tmp = Store.objects.filter(owner_id=user_pk)
	return len(tmp) == 0


@login_required
def change_store_owner_to_member(user):
	owners_group = Group.objects.get(name="store_owners")
	owners_group.user_set.remove(user)


@method_decorator(login_required, name='dispatch')
class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	@permission_required_or_403('REMOVE_ITEM',
	                            (Store, 'id', 'id'), accept_global_perms=True)
	def delete(self, request, *args, **kwargs):
		store = Store.objects.get(id=kwargs['pk'])
		owner_id = store.owner_id
		response = super(StoreDelete, self).delete(request, *args, **kwargs)
		if have_no_more_stores(owner_id):
			change_store_owner_to_member(request.user)
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


def buy_item(request, pk):
	if request.method == 'POST':
		form = BuyForm(request.POST)
		if form.is_valid():

			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			amount_in_db = _item.quantity
			if (amount <= amount_in_db):
				new_q = amount_in_db - amount
				_item.quantity = new_q
				_item.save()
				messages.success(request, 'YES! at the moment you bought  : ', _item.description)  # <-
				return redirect('/store/home_page_owner/')
			messages.warning(request, 'there is no such amount ! please try again!')
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')
	else:
		form_class = BuyForm
		curr_item = Item.objects.get(id=pk)
		context = {
			'pk': curr_item.id,
			'form': form_class,
			'price': curr_item.price,
			'description': curr_item.description
		}
		return render(request, 'store/buy_item.html', context)


@login_required
def home_page_owner(request):
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text
	}
	return render(request, 'store/homepage_store_owner.html', context)


class AddItemToStore(CreateView):
	model = Item
	fields = ['name', 'description', 'price', 'quantity']


def itemAddedSucceffuly(request, store_id, id):
	x = 1
	return render(request, 'store/item_detail.html')


@permission_required_or_403('ADD_MANAGER',
                            (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request, pk):
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			picked = form.cleaned_data.get('permissions')
			is_owner = form.cleaned_data.get('is_owner')
			user_ = User.objects.get(username=user_name)
			store_ = Store.objects.get(id=pk)
			if (user_ == None):
				messages.warning(request, 'no such user')
				return redirect('/store/home_page_owner/')
			for perm in picked:
				assign_perm(perm, user_, store_)
			if (is_owner):
				my_group = Group.objects.get(name="store_owners")
				user_.groups.add(my_group)
				store_.owners.add(user_)
			messages.success(request, 'add manager :  ' + user_name)
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')
	# do something with your results
	else:
		form = AddManagerForm
	return render(request, 'store/add_manager.html', {'form': form, 'pk': pk})
