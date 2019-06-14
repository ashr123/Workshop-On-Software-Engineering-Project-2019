from django.urls import path

from . import views

# from .views import ContactWizard,FORMS_

urlpatterns = [
	path('add_store/', views.add_store),
	path('add_item/<int:pk>', views.add_item),
	path('add_item_2/', views.AddItemToStore.as_view()),
	path('view_details/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
	path('delete/<int:pk>/', views.StoreDelete.as_view(success_url="/login_redirect")),
	path('add_item_to_store/<int:pk>/', views.add_item),
	path('buy_item/<int:pk>/', views.buy_item),
	path('update/<int:pk>', views.StoreUpdate.as_view(success_url="/login_redirect")),
	path('add_store/submit/', views.submit_open_store),
	path('add_item_to_store/<int:int>/<slug:id>', views.itemAddedSucceffuly, name='item-detail'),
	path('home_page_owner/', views.home_page_owner),
	path('view_store/', views.StoreListView.as_view(), name='store-owner-detail'),
	path('view_item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
	#
	path('buy_item/<int:pk>', views.buy_item),
	path('add_manager_to_store/<int:pk>', views.add_manager_to_store),
	path('add_manager_to_store/<int:pk>/', views.add_manager_to_store),
	path('add_discount_to_store/<int:pk>', views.add_discount_to_store),
	path('add_discount_to_store/<int:pk>/', views.add_discount_to_store),
	# path('update_item/<int:pk>/', views.update_item),
	path('update_item/<int:pk>/', views.ItemUpdate.as_view(success_url="/login_redirect")),
	# path('contact/<int:pk>/', ContactWizard.as_view(FORMS_)),
	path('store_owner_feed/<slug:owner_id>', views.owner_feed),
	path('add_rule_to_store/<int:pk>', views.add_rule_to_store),
	path('add_rule_to_store/<int:pk>/', views.add_rule_to_store),
	path('add_discount_to_item/<int:pk>/', views.add_discount_to_item),
	path('add_discount_to_item/<int:pk>', views.add_discount_to_item),
	# path('update_discount_to_item/', views.update_discount_view, name='ajax_load_cities')
]
