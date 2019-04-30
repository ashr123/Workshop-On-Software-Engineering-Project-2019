from django.shortcuts import render
from trading_system.forms import SearchForm
from store.models import Store, Item
from django.http import HttpResponse


# Create your views here.

def index(request):
	text = SearchForm()
	return render(request, 'homepage_guest.html', {'text': text})


def member(request):
	text = SearchForm()
	return render(request, 'homepage_member.html', {'text': text})


def register(request):
	return render(request, 'trading_system/register.html')


def search(request):
	text = SearchForm(request.GET)
	store = Store.objects.get(name="elhanan store")

	if text.is_valid():
		context = {'title': 'items', 'results': store.items}

	return render(request, 'search_results.html', context)


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
