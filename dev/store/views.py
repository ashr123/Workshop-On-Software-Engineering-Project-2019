from typing import Any, Union, Dict, List

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseRedirect, HttpResponse
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


def get_country_of_request(request: Any) -> str:
	return GeoIP2().country_name(get_client_ip(request))


@permission_required_or_403('ADD_ITEM', (Store, 'id', 'pk'))
@login_required
def add_item(request: Any, pk: int) -> Union[HttpResponseRedirect, HttpResponse]:
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			Store.objects.get(id=pk).items.add(form.save())  # item = form.save()
			messages.success(request, 'Your Item was added successfully!')  # <-
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, 'Problem with filed : ', form.errors, 'please try again!')  # <-
			return redirect('/store/home_page_owner/')
	else:
		print('\ndebug\n\n', pk)
		return render(request, 'store/add_item.html', {
			'store': pk,
			'form': ItemForm,
			'store_name': Store.objects.get(id=pk).name
		})


@login_required
def add_store(request: Any) -> HttpResponse:
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
def submit_open_store(request: Any) -> HttpResponseRedirect:
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             description=open_store_form.cleaned_data.get('description'))
		store.owners.add(request.user)
		store.save()
		messages.success(request, 'Your Store was added successfully!')
		Group.objects.get_or_create(name="store_owners")
		request.user.groups.add(Group.objects.get_or_create(name="store_owners")[0])
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

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


@method_decorator(login_required, name='dispatch')
class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
	permission_required = "@login_required"

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context

	def get_queryset(self) -> List[Store]:
		return Store.objects.filter(owners__id__in=[self.request.user.id])


class ItemListView(ListView):
	model = Item
	paginate_by = 100  # if pagination is desired


class ItemDetailView(DetailView):
	model = Item
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


@method_decorator(login_required, name='dispatch')
class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owners', 'items', 'description']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context

	def update(self, request, *args, **kwargs) -> HttpResponse:
		if not (self.request.user.has_perm('EDIT_ITEM')):
			messages.warning(request, 'there is no edit perm!')
			return render(request, 'homepage_member.html', {'text': SearchForm(), 'user_name': request.user.username})
		return super().update(request, *args, **kwargs)  # TODO check


def have_no_more_stores(user_pk: int) -> bool:
	return len(Store.objects.filter(owner_id=user_pk)) == 0


@login_required
def change_store_owner_to_member(user: User) -> None:
	Group.objects.get(name="store_owners").user_set.remove(user)


@method_decorator(login_required, name='dispatch')
class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	def delete(self, request, *args, **kwargs) -> HttpResponse:
		# craetor
		if not (self.request.user.has_perm('REMOVE_ITEM')):
			messages.warning(request, 'there is no delete perm!')
			return render(request, 'homepage_member.html',
			              {'text': SearchForm(), 'user_name': request.user.username})
		if have_no_more_stores(Store.objects.get(id=kwargs['pk']).owners.all()[0]):
			change_store_owner_to_member(request.user)
			return render(request, 'homepage_member.html',
			              {'text': SearchForm(), 'user_name': request.user.username})
		else:
			return super().delete(request, *args, **kwargs)

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()
		return context


def buy_item(request: Any, pk: int) -> HttpResponse:
	if request.method == 'POST':
		form = BuyForm(request.POST)
		if form.is_valid():

			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			if amount <= _item.quantity:
				_item.quantity = _item.quantity - amount
				_item.save()
				messages.success(request, 'YES! at the moment you bought  : ' + _item.description)  # <-
				messages.success(request, 'total : ' + str(amount * _item.price) + ' $')  # <-
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
			'description': curr_item.description,

		})


@login_required
def home_page_owner(request: Any) -> HttpResponse:
	return render(request, 'store/homepage_store_owner.html', {
		'user_name': request.user.username,
		'text': SearchForm()
	})


class AddItemToStore(CreateView):
	model = Item
	fields = ['name', 'description', 'price', 'quantity']


def itemAddedSucceffuly(request: Any, store_id: int, id: int) -> HttpResponse:  # TODO check
	return render(request, 'store/item_detail.html')


@permission_required_or_403('ADD_MANAGER', (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request: Any, pk: int) -> HttpResponseRedirect:
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			user_ = User.objects.get(username=user_name)
			store_ = Store.objects.get(id=pk)
			if user_name == request.user.username:
				messages.warning(request, 'can`t add yourself as a manager!')
				return redirect('/store/home_page_owner/')
			if user_ is None:
				messages.warning(request, 'no such user')
				return redirect('/store/home_page_owner/')
			for perm in form.cleaned_data.get('permissions'):
				assign_perm(perm, user_, store_)
			if form.cleaned_data.get('is_owner'):
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
