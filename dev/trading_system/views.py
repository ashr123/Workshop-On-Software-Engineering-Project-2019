from django.shortcuts import render
from trading_system.forms import  searchForm
# Create your views here.

def index(request):
    return render(request, 'homepage_guest.html')

def register(request):
    return render(request, 'trading_system/register.html')

def search(request):
