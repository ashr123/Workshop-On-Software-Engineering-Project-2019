import json
from typing import Any, Dict, List, Union

import django
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
# from external_systems.spellChecker import checker
from django.views.generic import DetailView
from django.views.generic.list import ListView

from dev.settings import PROJ_IP, PROJ_PORT
from store.models import Item, Store
from trading_system import service
from trading_system.forms import SearchForm, SomeForm, CartForm
# Create your views here.
from trading_system.models import Cart, Auction, CartGuest
from trading_system.observer import AuctionSubject
from .models import AuctionParticipant
from .routing import AUCTION_PARTICIPANT_URL

django.setup()

from django.contrib.auth.forms import UserCreationForm


def def_super_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			u = form.save()
			u.is_superuser = True
			u.is_staff = True
			u.save()
			messages.success(request, 'add super-user ' + str(u.username))
			return render(request, 'homepage_guest.html', {'text': SearchForm()})

		else:
			return redirect('/super_user')

	else:
		return render(request, 'trading_system/add_super_user.html', {'form': UserCreationForm()})


from django.contrib.auth.models import User


def index(request: Any) -> HttpResponse:
	superusers = User.objects.filter(is_superuser=True)
	if (len(superusers) == 0):
		return redirect('/super_user')
	else:
		return render(request, 'homepage_guest.html', {'text': SearchForm()})


def login_redirect(request: Any) -> Union[HttpResponseRedirect, HttpResponse]:
	if request.user.is_authenticated:
		if "store_owners" in request.user.groups.values_list('name',
		                                                     flat=True) or "store_managers" in request.user.groups.values_list(
			'name', flat=True):
			return redirect('/store/home_page_owner/',
			                {'text': SearchForm(), 'user_name': request.user.username, 'owner_id': request.user.pk, })
		else:

			return render(request, 'homepage_member.html', {'text': SearchForm(), 'user_name': request.user.username})

			return render(request, 'homepage_member.html',
			              {'text': text, 'user_name': user_name})

	return render(request, 'homepage_guest.html', {'text': SearchForm()})





def item(request: Any, id: int) -> HttpResponse:
	return render(request, 'trading_system/item_page.html', {
		'item': Item.objects.get(name=id)
	})


def show_cart(request: Any) -> HttpResponse:
	if request.user.is_authenticated:
		if "store_owners" in request.user.groups.values_list('name',
		                                                     flat=True) or "store_managers" in request.user.groups.values_list(
			'name', flat=True):
			base_template_name = 'store/homepage_store_owner.html'
		else:
			base_template_name = 'homepage_member.html'
		return render(request, 'cart.html', {
			'user_name': request.user.username,
			'text': SearchForm(),
			'base_template_name': base_template_name
		})
	else:
		base_template_name = 'homepage_guest.html'





class SearchListView(ListView):
	model = Item
	template_name = 'trading_system/search_results.html'

	def get_queryset(self):
		text = SearchForm(self.request.GET)
		if text.is_valid():
			# spell checker
			# correct_word = checker.Spellchecker(text)
			# items = Item.objects.filter(name=correct_word)
			return service.search(text.cleaned_data.get('search'))

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)  # get the default context data
		context['text'] = SearchForm()

	def get_context_data(self, **kwargs):
		text = SearchForm()
		context = super(SearchListView, self).get_context_data(**kwargs)  # get the default context data
		context['text'] = text

		return context


##ELHANANA - note that search returns the filtered items list
def search(request: Any) -> QuerySet:
	text = SearchForm(request.GET)
	if text.is_valid():
		# spell checker
		# correct_word = checker.Spellchecker(text)
		# items = Item.objects.filter(name=correct_word)
		return Item.objects.filter(Q(name__contains=text.cleaned_data.get('search')) | Q(
			description__contains=text.cleaned_data.get('search')) | Q(
			category__contains=text.cleaned_data.get('search')))


cart_index = 0





class CartDetail(DetailView):
	model = Cart

	def get_context_data(self, **kwargs) -> Dict[str, Any]:
		cart = Cart.objects.get(pk=kwargs['object'].pk)
		item_ids = list(map(lambda i: i.pk, cart.items.all()))
		context = super().get_context_data(**kwargs)  # get the default context data
		context['items'] = list(map(lambda i_pk: Item.objects.get(pk=i_pk), item_ids))

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

	def get_queryset(self) -> List[Cart]:
		return Cart.objects.filter(customer_id=self.request.user.pk)










########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


def register(request: Any) -> HttpResponse:
	return render(request, 'trading_system/register.html')

def home_button(request: Any) -> HttpResponseRedirect:
	return redirect('/login_redirect')


def approve_event(request: Any) -> HttpResponse:
	if request.method == 'POST':
		form = SomeForm(request.POST)
		if form.is_valid():
			# ('\n', form.cleaned_data.get('picked'))
			render(request, 'check_box_items.html', {'form': form})
		render(request, 'check_box_items.html', {'form': form})
	# do something with your results
	else:
		form = SomeForm
	return render(request, 'check_box_items.html', {'form': form})

from decimal import Decimal

from django.forms import formset_factory
from .forms import QForm

def make_cart_list(request: Any) -> Union[HttpResponseRedirect, HttpResponse]:
	# if not (request.user.is_authenticated):
	# 	return makeGuestCart(request)
	items_bought = []
	if request.method == 'POST':
		form = CartForm(request.user, makeGuestCart(request), request.POST)
		if form.is_valid():
			for item_id in form.cleaned_data.get('items'):
				# amount_in_db = Item.objects.get(id=item_id).quantity
				# if (amount_in_db > 0):
				if service.amount_in_db(item_id):
					try:
						quantity_to_buy = request.POST.get('quantity' + str(item_id))
						print('q----------------id:----' + str(item.id) + '------------' + quantity_to_buy)
					except:
						messages.warning(request, 'problem with quantity ')
					# item = Item.objects.get(id=item_id)
					# item.quantity = amount_in_db - 1
					# item.save()
					items_bought.append(item_id)
					if service.is_authenticated(request.user.pk):
						# cart = Cart.objects.get(customer=request.user)
						# cart.items.remove(item)
						service.remove_item_from_cart(request.user.pk, item_id)
					else:
						cartG = request.session['cart']
						cartG['items_id'].remove(Decimal(item_id))
						request.session['cart'] = cartG

					# if (item.quantity == 0):
					# 	item.delete()

				else:
					messages.warning(request, 'not enough amount of this item ')
					return redirect('/login_redirect')
			messages.success(request, 'Thank you! you just bought items from cart')

			return redirect('/login_redirect')

		err = '' + str(form.errors) + str(q.errors)
		messages.warning(request, 'error in :  ' + err)
		return redirect('/login_redirect')

	else:
		list_ = []
		if not (request.user.is_authenticated):
			base_template_name = 'homepage_guest.html'
			list_ = makeGuestCart(request)
		else:
			if "store_owners" in request.user.groups.values_list('name', flat=True):
				base_template_name = 'store/homepage_store_owner.html'
			else:
				base_template_name = 'homepage_member.html'

			list_ = None

		form = CartForm(request.user, list_)
		q_list = QForm(request.user, list_)
		text = SearchForm()
		user_name = request.user.username
		size_ = 0
		if (request.user.is_authenticated):
			carts = Cart.objects.filter(customer=request.user)
			items_of_user = []
			for cart in carts:
				items_of_user += list(cart.items.all())

			size_ = len(items_of_user)
		else:
			size_ = len(list_)
		context = {
			'user_name': user_name,
			'text': text,
			'form': form,
			'base_template_name': base_template_name,
			'qua': q_list,
		}
		return render(request, 'trading_system/cart_test.html', context)


def get_queryset(self):
	return Cart.objects.filter(customer_id=self.request.user.pk)


class AuctionsListView(ListView):
	model = Auction
	template_name = 'trading_system/user_auctions.html'

	def get_queryset(self):
		return Auction.objects.filter(
			auctionparticipant__customer=self.request.user.pk
		)


def join_auction(request, item_pk):
	try:
		auction = Auction.objects.get(item_id=item_pk)
	except ObjectDoesNotExist:
		auction = Auction.objects.create(item_id=item_pk)
	ap = AuctionParticipant(auction_id=auction.pk, customer_id=request.user.pk, offer=3,
	                        address="ws://{}:{}/ws/{}/{}/{}/".format(PROJ_IP, PROJ_PORT, AUCTION_PARTICIPANT_URL,
	                                                                 item_pk, request.user.pk))
	context = {'action_desc': ''}
	try:
		ap.save()
		context['action_desc'] = 'You joined the auction'
	except django.db.IntegrityError as e:
		context['action_desc'] = 'You have already joined this auction'
	auction_subject = AuctionSubject(auction_id=auction.pk)
	auction_subject._notify()
	return render(request, 'trading_system/action_happend_succefully.html', context)


def view_auction(request, auction_pk):
	auction = Auction.objects.get(id=auction_pk)
	context = {
		'participant_id_json': mark_safe(json.dumps(request.user.pk)),
		'participant_id': request.user.pk,
		'item_id': auction.item_id,
		'url': AUCTION_PARTICIPANT_URL
	}
	return render(request, 'trading_system/auction_feed.html', context)


# def get_item_store(item_pk):
# 	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))
# 	# Might cause bug. Need to apply the item-in-one-store condition
# 	return stores[0]


def add_item_to_cart(request, item_pk):
	ans = service.add_item_to_cart(request.user.pk, item_pk)
	if ans is True:
		messages.success(request, 'add to cart successfully')
		return redirect('/login_redirect')
	else:
		if 'cart' in request.session:
			cartG = request.session['cart']
			cartG['items_id'].append(item_pk)
		else:
			cartG = CartGuest([item_pk]).serialize()

		request.session['cart'] = cartG
		messages.success(request, 'add to cart successfully')
		return redirect('/login_redirect')


# if (request.user.is_authenticated):
# 	item_store = get_item_store(item_pk)
# 	cart = get_cart(item_store, request.user.pk)
# 	if cart is None:
# 		open_cart_for_user_in_store(item_store.pk, request.user.pk)  # TODO
# 		cart = get_cart(item_store, request.user.pk)
# 	cart.items.add(item_pk)
# 	messages.success(request, 'add to cart successfully')
# 	return redirect('/login_redirect')
# else:
# 	if 'cart' in request.session:
# 		cartG = request.session['cart']
# 		cartG['items_id'].append(item_pk)
# 	else:
# 		cartG = CartGuest([item_pk]).serialize()
#
# 	request.session['cart'] = cartG
#
# 	messages.success(request, 'add to cart successfully')
# 	return redirect('/login_redirect')


# def get_item_store(item_pk):
# 	stores = list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))
#
# 	# Might cause bug. Need to apply the item-in-one-store condition
# 	return list(filter(lambda s: item_pk in map(lambda i: i.pk, s.items.all()), Store.objects.all()))[0]


# def open_cart_for_user_in_store(store_pk: int, user_pk: int) -> None:
# 	Cart(customer_id=user_pk, store_id=store_pk).save()


# def get_cart(store_pk, user_pk):
# 	carts = Cart.objects.filter(customer_id=user_pk, store_id=store_pk)
# 	if len(carts) == 0:
# 		return None
# 	else:
# 		return carts[0]

def makeGuestCart(request):
	if (service.is_authenticated(request.user.pk)):
		return []
	items_ = []
	cartG = request.session['cart']
	id_list = cartG['items_id']
	for id in id_list:
		items_ += list([service.get_item(id)])
	return items_
