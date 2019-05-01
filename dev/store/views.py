from django.shortcuts import render
from django.conf import settings
from .models import Store, Item
from . import forms
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.edit import CreateView


# Create your views here.
def add_store(request):
	name = forms.OpenStoreForm()
	return render(request, 'store/add_store.html', {'name': name})


def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             owner_id=int(request.session._session['_auth_user_id']))
		# item1 = Item(name='dd')
		# item1.save()
		# store.items.add(item1)
		store.save()

	stores = Store.objects.get(owner_id=int(request.session._session['_auth_user_id']))

	context = {'title': 'stores:', 'results': stores}

	return render(request, 'store/homepage_store_owner.html', context)


class StoreDetailView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired


class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
