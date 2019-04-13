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
        f = open("rotem.txt", "a")
        f.write(form.user_name)
        f.close()
        # check whether it's valid:
    facade = ServiceFacade()
    facade.setup("as", "asd")
    now = datetime.datetime.now()
    html = "<html><body>It is xdsfdsfsdfdsnow %s.</body></html>" % now
    return render_to_response('home_after.html')

