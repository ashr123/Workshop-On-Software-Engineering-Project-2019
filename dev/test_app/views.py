from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from .forms import ContactForm
from .forms import AuthorForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            tmp = form.cleaned_data['your_name']
            return HttpResponseRedirect('/test/test1/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'test_app/test_page1.html', {'form': form})

def thanks(request):
	return render(request, 'test_app/response.html')


def get_contact(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/test/test1/thanks/')
	else:
		form = ContactForm()

	return render(request, 'test_app/test_page2.html', {'form': form})

def noa(request):
	return render(request, 'test_app/test_page3.html')


def test4(request):
	if request.method == 'POST':
		form = AuthorForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/test/test1/thanks/')
	else:
		form = AuthorForm()

	return render(request, 'test_app/test_page4.html', {'form': form})