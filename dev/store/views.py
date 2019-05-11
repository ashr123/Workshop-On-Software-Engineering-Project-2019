from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, redirect
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


@permission_required_or_403('ADD_ITEM', (Store, 'id', 'pk'))
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
		curr_store = Store.objects.get(id=pk)
		print('\ndebug\n\n', pk)
		return render(request, 'store/add_item.html', {
			'store': pk,
			'form': ItemForm,
			'store_name': curr_store.name
		})


@login_required
def add_store(request):
	# g = GeoIP2()
	# print('\n\ncountry :  ',get_country_of_request(request))
	# print('\n\ncountry :  ', g.country('132.73.202.157'))
	if "store_owners" in request.user.groups.values_list('name', flat=True):
		base_template_name = 'store/homepage_store_owner.html'
	else:
		base_template_name = 'homepage_member.html'
	return render(request, 'store/add_store.html', {
		'set_input': forms.OpenStoreForm(),
		'user_name': request.user.username,
		'text': SearchForm(),
		'base_template_name': base_template_name
	})


@login_required
def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             description=open_store_form.cleaned_data.get('description'))
		store.owners.add(request.user)
		store.save()
		messages.success(request, 'Your Store was added successfully!')
		# my_group = Group.objects.get(name="store_owners")
		request.user.groups.add(Group.objects.get_or_create(name="store_owners"))
		assign_perm('ADD_ITEM', request.user, store)
		assign_perm('REMOVE_ITEM', request.user, store)
		assign_perm('EDIT_ITEM', request.user, store)
		assign_perm('ADD_MANAGER', request.user, store)
		return redirect('/store/home_page_owner')
	else:
		messages.warning(request, 'Please correct the error and try again.')
		return redirect('/login_redirect')


# need to be in the first time:

@method_decorator(login_required, name='dispatch')
class StoreDetailView(DetailView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		context = super(StoreDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		context = super(StoreListView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context

	def get_queryset(self):
		# return Store.objects.filter(owner_id=self.request.user.id)
		return Store.objects.filter(owners__id__in=[self.request.user.id])


class ItemListView(ListView):
	model = Item
	paginate_by = 100  # if pagination is desired


class ItemDetailView(DetailView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


@method_decorator(login_required, name='dispatch')
class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owners', 'items', 'description']
	template_name_suffix = '_update_form'
	permission_required = "@login_required"

	def get_context_data(self, **kwargs):
		context = super(StoreUpdate, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
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
	return len(Store.objects.filter(owner_id=user_pk)) == 0


@login_required
def change_store_owner_to_member(user):
	Group.objects.get(name="store_owners").user_set.remove(user)


@method_decorator(login_required, name='dispatch')
class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	@permission_required_or_403('REMOVE_ITEM', (Store, 'id', 'id'), accept_global_perms=True)
	def delete(self, request, *args, **kwargs):
		owner_id = Store.objects.get(id=kwargs['pk']).owner_id
		if have_no_more_stores(owner_id):
			change_store_owner_to_member(request.user)
			return render(request, 'homepage_member.html', {'text': SearchForm(), 'user_name': request.user.username})
		else:
			return super(StoreDelete, self).delete(request, *args, **kwargs)  # response

	def get_context_data(self, **kwargs):
		context = super(StoreDelete, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


def buy_item(request, pk):
	if request.method == 'POST':
		form = BuyForm(request.POST)
		if form.is_valid():

			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			amount_in_db = _item.quantity
			if (amount <= amount_in_db):
				_item.quantity = amount_in_db - amount
				_item.save()
				messages.success(request, 'YES! at the moment you bought  : ', _item.description)  # <-
				return redirect('/store/home_page_owner/')
			messages.warning(request, 'there is no such amount ! please try again!')
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')
	else:
		curr_item = Item.objects.get(id=pk)
		return render(request, 'store/buy_item.html', {
			'pk': curr_item.id,
			'form': BuyForm,
			'price': curr_item.price,
			'description': curr_item.description
		})


@login_required
def home_page_owner(request):
	return render(request, 'store/homepage_store_owner.html', {
		'user_name': request.user.username,
		'text': SearchForm()
	})


class AddItemToStore(CreateView):
	model = Item
	fields = ['name', 'description', 'price', 'quantity']


def itemAddedSucceffuly(request, store_id, id):
	return render(request, 'store/item_detail.html')


@permission_required_or_403('ADD_MANAGER', (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request, pk):
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			is_owner = form.cleaned_data.get('is_owner')
			user_ = User.objects.get(username=user_name)
			store_ = Store.objects.get(id=pk)
			if (user_ == None):
				messages.warning(request, 'no such user')
				return redirect('/store/home_page_owner/')
			for perm in form.cleaned_data.get('permissions'):
				assign_perm(perm, user_, store_)
			if (is_owner):
				user_.groups.add(Group.objects.get(name="store_owners"))
				store_.owners.add(user_)
			messages.success(request, 'add manager :  ' + user_name)
			return redirect('/store/home_page_owner/')
		messages.warning(request, 'error in :  ', form.errors)
		return redirect('/store/home_page_owner/')
	# do something with your results
	else:
		form = AddManagerForm
	return render(request, 'store/add_manager.html', {'form': form, 'pk': pk})


def owner_feed(request, owner_id):
	return render(request, 'store/owner_feed.html', {
		# 'owner_id_json': mark_safe(json.dumps(owner_id)),
		'owner_id': owner_id
	})
