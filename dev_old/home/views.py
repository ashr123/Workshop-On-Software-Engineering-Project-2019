import datetime

from django.shortcuts import render, render_to_response
from main.service.ServiceFacade import ServiceFacade

from django.http import HttpResponse
from .forms import InitiateForm

def index(request):
    return render_to_response('home_page.html')


def initiate(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InitiateForm(request.POST)
        print("asdasd")
        if form.is_valid():
            print("asdasd")
            name = form.cleaned_data['your_name']
            f = open("rotem.txt", "a")
            f.write(name)
            f.close()
        else:
            print(form.errors)
        # check whether it's valid:
    facade = ServiceFacade()
    facade.setup("as", "asd")
    now = datetime.datetime.now()
    return render(request, 'home_page.html')

