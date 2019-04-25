from django.shortcuts import render
from trading_system.forms import SearchForm
from django.http import HttpResponse


# Create your views here.

def index(request):
    text = SearchForm()
    return render(request, 'trading_system/homepage_guest.html', {'text': text})


def register(request):
    return render(request, 'trading_system/register.html')


def search(request):
    text = SearchForm(request.GET)
    if text.is_valid():
        return HttpResponse("yesss " + text)

    return HttpResponse("noo " + text)



