from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'trading_system/index.html')

def register(request):
    return render(request, 'trading_system/register.html')