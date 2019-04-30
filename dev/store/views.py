from django.shortcuts import render
from django.conf import settings
from .models import Store, Item
from . import forms


# Create your views here.
def add_store(request):
	name = forms.OpenStoreForm()
	return render(request, 'store/add_store.html', {'name': name})


def submit_open_store(request):
	open_store_form = forms.OpenStoreForm(request.GET)
	if open_store_form.is_valid():
		store = Store.objects.create(name=open_store_form.cleaned_data.get('name'),
		                             owner_id=int(request.session._session['_auth_user_id']))
		item1 = Item(name='dd')
		item1.save()
		store.items.add(item1)
		store.save()

	stores = Store.objects.get(owner_id=int(request.session._session['_auth_user_id']))

	context = {'title': 'stores:', 'results': stores}

	return render(request, 'homepage_store_owner.html', context)
