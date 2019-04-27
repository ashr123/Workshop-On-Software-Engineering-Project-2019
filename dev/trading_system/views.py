from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'trading_system/index.html')

def register(request):
	return render(request, 'trading_system/register.html')


def search(request):
	text = SearchForm(request.GET)
	if text.is_valid():
		context = {'title': 'items', 'results': {'3': 4, '2': 6}}

	return render(request, 'search_results.html', context)


def item(request, id):
	return render(request, 'item_de.html')
