from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('actionUrl/', views.search),
    path('homepage_member', views.member),
]
