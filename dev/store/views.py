from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.forms import modelformset_factory
from trading_system.forms import SearchForm
from . import forms
from .forms import ItemForm
from .models import Store
from .models import Item


def add_item(request, pk):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			item = form.save()
			curr_store = Store.objects.get(id=pk)
			curr_store.items.add(item)
			return redirect('/store/home_page_owner/')
		return HttpResponse('error in :  ', form.errors)
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



def add_store(request):
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

def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             owner_id=int(request.session._session['_auth_user_id']),
		                             description=open_store_form.cleaned_data.get('description'))
		store.save()

	# need to be in the first time:
	my_group = Group.objects.get_or_create(name="store_owners")
	my_group = Group.objects.get(name="store_owners")

	request.user.groups.add(my_group)
	return redirect('/store/home_page_owner')


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
		text = SearchForm()
		context = super(StoreListView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context

	def get_queryset(self):
		return Store.objects.filter(owner_id=self.request.user.id)


class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owner', 'items']
	template_name_suffix = '_update_form'


def have_no_more_stores(user_pk):
	tmp = Store.objects.filter(owner_id=user_pk)
	return len(tmp) == 0


def change_store_owner_to_member(user):
	owners_group = Group.objects.get(name="store_owners")
	owners_group.user_set.remove(user)


class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'

	def delete(self, request, *args, **kwargs):
		store = Store.objects.get(id = kwargs['pk'])
		owner_id = store.owner_id
		response = super(StoreDelete, self).delete(request, *args, **kwargs)
		if have_no_more_stores(owner_id):
			change_store_owner_to_member(request.user)
			user_name = request.user.username
			text = SearchForm()
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})
		else:
			return response


def buy_item(request, pk):
	return 0

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
