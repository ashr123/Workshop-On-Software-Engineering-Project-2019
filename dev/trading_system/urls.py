from django.urls import path

from . import views

urlpatterns = [
	path('', views.index),
	# path(r'^item_page/(?P<id>\d+)/$', views.item),
	path('item_page/<int:id>/', views.item),
	path('home_button/', views.home_button),
	path('login_redirect', views.login_redirect),
	path('cart/', views.show_cart),
	path('show_cart', views.make_cart_list),
	path('show_cart/', views.make_cart_list),
	path('view_items/', views.SearchListView.as_view(), name='item-list'),
	path('add_item_to_cart/<int:item_pk>', views.add_item_to_cart),
	path('view_carts', views.CartsListView.as_view()),
	path('view_cart/<int:pk>', views.CartDetail.as_view()),
	path('approve_event/', views.approve_event),

]
