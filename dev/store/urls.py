from django.urls import path
from . import views

urlpatterns = [
		path('add_store/', views.add_store),
		path('add_store/submit/', views.submit_open_store),
]
