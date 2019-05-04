from django.urls import path
from . import views
from store import views as store_views

urlpatterns = [
	path('', views.index),
	path(r'^item_page/(?P<id>\d+)/$', views.item),
	path('home_button/', views.home_button),
	path('view_items/', store_views.ItemListView.as_view(), name='item-list',),
	path('login_redirect', views.login_redirect),
	path('cart/', views.show_cart),
	path('view_items/', store_views.ItemListView.as_view(), name='item-list',)
]
