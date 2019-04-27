from django.shortcuts import render
from trading_system.forms import SearchForm
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
	if text.is_valid():
		context = {'title': 'items', 'results': [{id: 1}, {id: 2}]}

	return render(request, 'search_results.html', context)


def item(request, id):
	return render(request, 'item_de.html')
