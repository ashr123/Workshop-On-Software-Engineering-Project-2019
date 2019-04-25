from django.shortcuts import render
from trading_system.forms import SearchForm
from django.http import HttpResponse


# Create your views here.

def index(request):
    text = SearchForm()
    return render(request, 'homepage_member.html', {'text': text})


def register(request):
    return render(request, 'trading_system/register.html')


def search(request):
    text = SearchForm(request.GET)
    if text.is_valid():
        return HttpResponse("yes " + text.cleaned_data['text'])
    return HttpResponse("no " + text.cleaned_data['text'])


