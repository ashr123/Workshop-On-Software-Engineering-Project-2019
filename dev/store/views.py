from django.shortcuts import render
from django.conf import settings
from .models import Store, Item
from . import forms
from django.contrib.auth.models import Group ,User

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

	my_group = Group.objects.get(name='store_owners')
	#my_group.user_set.add(request.user)
	# user = User.objects.get(username=request.user.username)
	request.user.groups.add(my_group)

	stores = Store.objects.get(owner_id=int(request.session._session['_auth_user_id']))[0]

	context = {'title': 'stores:', 'results': stores}

	return render(request, 'homepage_store_owner.html', context)
