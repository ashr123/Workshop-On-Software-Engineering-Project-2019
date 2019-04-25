from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from trading_system.forms import SearchForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


# def logout_view(request):
#     text = SearchForm()
#     logout(request)
#     next = request.POST.get('next', '/')
#     return HttpResponseRedirect(next)
#     #return redirect('homepage_guest.html', {'text': text})
#
#
# # return render(request, 'homepage_guest.html', {'text': text})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
