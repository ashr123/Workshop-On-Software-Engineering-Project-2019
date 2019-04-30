from django.shortcuts import render


# Create your views here.

def index(request):
	return render(request, 'test_app/test_page.html')