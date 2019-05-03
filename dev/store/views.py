from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.views.generic import DetailView

from .models import Store, Item
from . import forms
from django.contrib.auth.models import Group, User
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.forms import modelformset_factory
from trading_system.forms import SearchForm



def add_item(request, pk):
	item_f = forms.ItemForm(request.POST)
	# ItemFormSet = modelformset_factory(Item, fields=('name', 'description', 'price', 'category', 'quantity'))
	# 	# if request.method == "POST":
	# 	# 	formset = ItemFormSet(
	# 	# 		request.POST, request.FILES,
	# 	# 		queryset=Item.objects.filter(),
	# 	# 	)
	# 	#
	# 	# 	if formset.is_valid():
	# 	# 		store_name = request['store']
	# 	# 		formset.save()
	# 	# 		return HttpResponse(store_name)
	if item_f.is_valid():
		# item = Item.objects.create(name=item_f.cleaned_data.get('name'),description=item_f.cleaned_data.get('description')
		#                              ,price=item_f.cleaned_data.get('price'),category=item_f.cleaned_data.get('category'),quantity=item_f.cleaned_data.get('quantity'))
		# curr_store = Store.objects.get(id=pk)
		# item.save()
		# curr_store.items.add(item)
		# return redirect('/store/home_page_owner/')
		name = item_f.cleaned_data['name']
		return HttpResponse(name)
	return HttpResponse(" fail ")


def add_item_to_store(request, pk):
	ItemFormSet = modelformset_factory(Item, fields=('name', 'description', 'price', 'category', 'quantity'))
	# ItemFormSet = modelformset_factory(Item, formset=ItemForm,
	#                                    fields=('name', 'description', 'price', 'category', 'quantity', 'store_id'))
	# if request.method == "POST":
	# 	formset = ItemFormSet(
	# 		request.POST, request.FILES,
	# 		queryset=Item.objects.filter(),
	# 	)
	#
	# 	if formset.is_valid():
	# 		formset.save()
	# # Do something.
	# else:
	formset = ItemFormSet(queryset=Item.objects.filter(name__startswith='O'))

	# curr_store = Store.objects.get(id=pk)
	# store_name = curr_store.name
	context = {
		'store': pk,
		'formset': formset,
	}
	return render(request, 'store/add_item.html', context)


# item = ItemForm()
# return render(request, 'store/add_item.html', {'item': item})

# Create your views here.
def add_store(request):
	name = forms.OpenStoreForm()

	return render(request, 'store/add_store.html', {'name': name})


def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             owner_id=int(request.session._session['_auth_user_id']))
		store.save()
	# in error masssege!!!!!!!!!!!!!
	# stores = Store.objects.filter(owner_id=int(request.session._session['_auth_user_id']))

	# need to be in the first time:
	my_group = Group.objects.get_or_create(name="store_owners")

	my_group = Group.objects.get(name="store_owners")
	# user = User.objects.get(username=request.user.username)
	request.user.groups.add(my_group)
	# stores = Store.objects.get(owner_id=int(request.session._session['_auth_user_id']))[0]
	# context = {'title': 'stores:', 'results': stores}
	# return render(request, 'store/homepage_store_owner.html', context)
	return redirect('/store/home_page_owner/')


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


class StoreUpdate(UpdateView):
	model = Store
	fields = ['name', 'owner', 'items']
	template_name_suffix = '_update_form'


class StoreDelete(DeleteView):
	model = Store
	template_name_suffix = '_delete_form'


def buy_item(request, pk):
	return 0


