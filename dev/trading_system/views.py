from django.shortcuts import render, redirect, render_to_response
# from external_systems.spellChecker import checker
from django.views.generic import DetailView
from django.views.generic.list import ListView

from store.models import Item
from store.models import Store
from trading_system.forms import SearchForm, SomeForm
# Create your views here.
from trading_system.models import Cart


def index(request):
	text = SearchForm()
	return render(request, 'homepage_guest.html', {'text': text})


def login_redirect(request):
	text = SearchForm()

	if request.user.is_authenticated:
		user_name = request.user.username
		user_groups = request.user.groups.values_list('name', flat=True)
		if request.user.is_superuser:
			return render(request, 'homepage_member.html', {'text': text})
		elif "store_owners" in user_groups:
			return redirect('/store/home_page_owner/', {'text': text, 'user_name': user_name})
		else:
			return render(request, 'homepage_member.html', {'text': text, 'user_name': user_name})

	return render(request, 'homepage_guest.html', {'text': text})


def register(request):
	return render(request, 'trading_system/register.html')


def item(request, id):
	item = Item.objects.get(name=id)
	context = {
		'item': item
	}

	return render(request, 'trading_system/item_page.html', context)


def item(request, id):
	item = Item.objects.get(name=id)
	context = {
		'item': item
	}
	# store = Store.objects.get(name=name_)
	# context = {
	# 	'store': store
	# }
	return render(request, 'trading_system/item_page.html', context)


def show_cart(request):
	user_groups = request.user.groups.values_list('name', flat=True)
	if request.user.is_authenticated:
		if "store_owners" in user_groups:
			base_template_name = 'store/homepage_store_owner.html'
		else:
			base_template_name = 'homepage_member.html'
	else:
		base_template_name = 'homepage_guest.html'
	text = SearchForm()
	user_name = request.user.username
	context = {
		'user_name': user_name,
		'text': text,
		'base_template_name': base_template_name
	}
	return render_to_response('cart.html', context)


def home_button(request):
	return redirect('/login_redirect')


class SearchListView(ListView):
	model = Item
	template_name = 'trading_system/search_results.html'

	def get_queryset(self):
		return search(self.request)

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(SearchListView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text
		return context


##ELHANANA - note that search returns the filtered items list
def search(request):
	text = SearchForm(request.GET)
	if text.is_valid():
		# spell checker
		# correct_word = checker.Spellchecker(text)
		# items = Item.objects.filter(name=correct_word)
		return Item.objects.filter(name__contains=text.cleaned_data.get('search'))


def add_item_to_cart(request, item_pk):
	item_store = get_item_store(item_pk)
	cart = get_cart(item_store, request.user.pk)
	if cart == None:
		open_cart_for_user_in_store(item_store.pk, request.user.pk)
		cart = get_cart(item_store, request.user.pk)
	cart.items.add(item_pk)
	return render(request, 'trading_system/item_added_successfuly.html')


def get_item_store(item_pk):
	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))
	# Might cause bug. Need to apply the item-in-one-store condition
	return stores[0]


def user_has_cart_for_store(store_pk, user_pk):
	return len(Cart.objects.filter(customer_id=user_pk, store_id=store_pk)) > 0


def open_cart_for_user_in_store(store_pk, user_pk):
	cart = Cart(customer_id=user_pk, store_id=store_pk)
	cart.save()


def get_cart(store_pk, user_pk):
	carts = Cart.objects.filter(customer_id=user_pk, store_id=store_pk)
	if len(carts) == 0:
		return None
	else:
		return carts[0]


class CartDetail(DetailView):
	model = Cart

	def get_context_data(self, **kwargs):
		cart = Cart.objects.get(pk=kwargs['object'].pk)
		item_ids = list(map(lambda i: i.pk, cart.items.all()))
		items = list(map(lambda i_pk: Item.objects.get(pk=i_pk), item_ids))
		context = super(CartDetail, self).get_context_data(**kwargs)  # get the default context data
		context['items'] = items
		context['store_name'] = Store.objects.get(pk=cart.store_id).name
		return context


class CartsListView(ListView):
	model = Cart
	template_name = 'trading_system/user_carts.html'

	def get_queryset(self):
		return Cart.objects.filter(customer_id=self.request.user.pk)


def approve_event(request):
	if request.method == 'POST':
		form = SomeForm(request.POST)
		if form.is_valid():
			picked = form.cleaned_data.get('picked')
			print('\n', picked)
			render(request, 'check_box_items.html', {'form': form})
		render(request, 'check_box_items.html', {'form': form})
	# do something with your results
	else:
		form = SomeForm
	return render(request, 'check_box_items.html', {'form': form})
