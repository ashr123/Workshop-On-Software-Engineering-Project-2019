from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('initiate', views.initiate),
	path('', RedirectView.as_view(url='/home/', permanent=True))
]
