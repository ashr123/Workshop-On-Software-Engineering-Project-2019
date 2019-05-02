from django.shortcuts import render , redirect
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
		user_groups = request.user.groups.values_list('name', flat=True)
		if request.user.is_superuser:
			return render(request, 'homepage_member.html', {'text': text})
		elif "store_owners" in user_groups:
			return redirect('/store/home_page_owner/', {'text': text})
		else:
			return render(request, 'homepage_member.html', {'text': text})

	return render(request, 'homepage_guest.html', {'text': text})


def register(request):
	return render(request, 'trading_system/register.html')


def search(request):
	text = SearchForm(request.GET)

	#spell checker

	if text.is_valid():
		items = Item.objects.filter(name=text)
		context = {'title': 'items: ', 'results': items}
	return render(request, 'search_results.html', context)


def item(request, id):
	item = Item.objects.get(name=id)
	context = {
		'item': item
	}

	return render(request, 'item_page.html', context)
