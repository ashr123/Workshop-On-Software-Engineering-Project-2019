from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
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


@permission_required_or_403('ADD_ITEM', (Store, 'id', 'pk'))
@login_required
def add_item(request, pk):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			item = form.save()
			Store.objects.get(id=pk).items.add(item)
			messages.success(request, 'Your Item was added successfully!')  # <-
			return redirect('/store/home_page_owner/')
		else:
			messages.warning(request, 'Problem with filed: ', form.errors, 'please try again!')  # <-
			return redirect('/store/home_page_owner/')
	else:
		print('\ndebug\n\n', pk)
		return render(request, 'store/add_item.html', {
			'store': pk,
			'form': ItemForm,
			'store_name': Store.objects.get(id=pk).name
		})


@login_required
def add_store(request):
	return render(request, 'store/add_store.html', {
		'set_input': forms.OpenStoreForm(),
		'user_name': request.user.username,
		'text': SearchForm(),
		'base_template_name':
			'store/homepage_store_owner.html'
			if "store_owners" in request.user.groups.values_list('name', flat=True)
			else 'homepage_member.html'
	})


@login_required
def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             description=open_store_form.cleaned_data.get('description'))
		store.owners.add(request.user)
		store.save()
		messages.success(request, 'Your Store was added successfully!')  # <-
		# my_group = Group.objects.get_or_create(name="store_owners")
		request.user.groups.add(Group.objects.get(name="store_owners"))
		assign_perm('ADD_ITEM', request.user, store)
		assign_perm('REMOVE_ITEM', request.user, store)
		assign_perm('EDIT_ITEM', request.user, store)
		assign_perm('ADD_MANAGER', request.user, store)
		return redirect('/store/home_page_owner')
	else:
		messages.warning(request, 'Please correct the error and try again.')  # <-
		return redirect('/login_redirect')


# need to be in the first time:


class StoreDetailView(DetailView):
	model = Store
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(StoreDetailView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired

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


class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owners', 'items']
	template_name_suffix = '_update_form'


def have_no_more_stores(user_pk):
	return len(Store.objects.filter(owner_id=user_pk)) == 0


@login_required
def change_store_owner_to_member(user):
	Group.objects.get(name="store_owners").user_set.remove(user)


class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	def delete(self, request, *args, **kwargs):
		if have_no_more_stores(Store.objects.get(id=kwargs['pk']).owner_id):
			change_store_owner_to_member(request.user)
			return render(request, 'homepage_member.html', {'text': SearchForm(), 'user_name': request.user.username})
		else:
			return super(StoreDelete, self).delete(request, *args, **kwargs)  # response


@login_required
def buy_item(request, pk):
	if request.method == 'POST':
		form = BuyForm(request.POST)
		if form.is_valid():
			_item = Item.objects.get(id=pk)
			amount = form.cleaned_data.get('amount')
			if amount <= _item.quantity:
				_item.quantity -= amount
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


def item_added_ssuccefuly(request):
	return render(request, 'store/item_detail.html')


@permission_required_or_403('ADD_MANAGER', (Store, 'id', 'pk'))
@login_required
def add_manager_to_store(request, pk):
	if request.method == 'POST':
		form = AddManagerForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data.get('user_name')
			user_ = User.objects.get(username=user_name)
			store_ = Store.objects.get(id=pk)
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
