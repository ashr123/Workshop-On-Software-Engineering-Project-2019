# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup.html'),
	# path('signup/', views.SignUp.as_view(), name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
	# path('signup/', auth_views.SigView.as_view(template_name='signup.html')),

]
