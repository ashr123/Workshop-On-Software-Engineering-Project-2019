from django.shortcuts import render,redirect
from django.conf import settings
from django.views.generic import DetailView

from .models import Store, Item
from . import forms
from django.contrib.auth.models import Group, User
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
		store.save()
	# in error masssege!!!!!!!!!!!!!
	# stores = Store.objects.filter(owner_id=int(request.session._session['_auth_user_id']))
	my_group = Group.objects.get(name="store_owners")
	# user = User.objects.get(username=request.user.username)
	request.user.groups.add(my_group)
	# stores = Store.objects.get(owner_id=int(request.session._session['_auth_user_id']))[0]
	#context = {'title': 'stores:', 'results': stores}
	#return render(request, 'store/homepage_store_owner.html', context)
	return redirect('/store/home_page_owner/')

class StoreDetailView(DetailView):
	model = Store
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class StoreListView(ListView):
	model = Store
	paginate_by = 100  # if pagination is desired
