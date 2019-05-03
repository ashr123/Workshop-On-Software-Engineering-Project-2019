from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path(r'^item_page/(?P<id>\d+)/$', views.item),
	path('home_button/', views.home_button),
	path('actionUrl/', views.search),
	path('login_redirect', views.login_redirect),
	path('cart_guest/', views.show_cart_guest),
	path('cart_member/', views.show_cart_member)
]
