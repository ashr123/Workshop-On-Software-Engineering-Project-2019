from django.shortcuts import render, redirect

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
		print('\n\n', text.cleaned_data.get('search'))
		items = Item.objects.filter(name=text.cleaned_data.get('search'))

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


def show_cart_guest(request):
	text = SearchForm()
	return render(request, 'cart_guest.html', {'text': text})

def show_cart_member(request):
	text = SearchForm()
	return render(request, 'cart_member.html', {'text': text})


def home_button(request):
	return redirect('/login_redirect')
