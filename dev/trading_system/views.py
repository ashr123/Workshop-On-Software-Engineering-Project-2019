from django.shortcuts import render, redirect, render_to_response

# from external_systems.spellChecker import checker
from trading_system.forms import SearchForm
from store.models import Store, Item
from django.http import HttpResponse


# Create your views here.

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
			return redirect('/store/home_page_owner/', {'text': text,'user_name' : user_name})
		else:
			return render(request, 'homepage_member.html', {'text': text,'user_name' : user_name})

	return render(request, 'homepage_guest.html', {'text': text})


def register(request):
	return render(request, 'trading_system/register.html')


def search(request):
	text = SearchForm(request.GET)

	if text.is_valid():
		# spell checker
		# correct_word = checker.Spellchecker(text)
		# items = Item.objects.filter(name=correct_word)

		items = Item.objects.filter(name=text)
		context = {'title': 'items: ', 'results': items}
	return render(request, 'search_results.html', context)


def item(request, id):
	item = Item.objects.get(name=id)
	context = {
		'item': item
	}

	return render(request, 'item_page.html', context)


def item(request, id):
	item = Item.objects.get(name=id)
	context = {
		'item': item
	}
	# store = Store.objects.get(name=name_)
	# context = {
	# 	'store': store
	# }
	return render(request, 'item_page.html', context)



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
