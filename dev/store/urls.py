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
	path('add_discount_to_store/<int:pk>/<slug:which_button>', views.add_discount_to_store),
	path('add_discount_to_store/<int:pk>/<slug:which_button>/', views.add_discount_to_store),
	path('add_complex_discount_to_store/<int:pk>/<slug:disc>/<slug:which_button>', views.add_complex_discount_to_store),
	path('add_complex_discount_to_store/<int:pk>/<slug:disc>/<slug:which_button>/', views.add_complex_discount_to_store),
	# path('update_item/<int:pk>/', views.update_item),
	path('update_item/<int:pk>/', views.ItemUpdate.as_view(success_url="/login_redirect")),
	# path('contact/<int:pk>/', ContactWizard.as_view(FORMS_)),
	path('add_base_rule_to_store/<int:pk>/<slug:which_button>', views.add_base_rule_to_store),
	path('add_base_rule_to_store/<int:pk>/<slug:which_button>/', views.add_base_rule_to_store),
	path('store_owner_feed/<slug:owner_id>', views.NotificationsListView.as_view(), name='owner-feed'),
	# path('add_discount_to_item/<int:pk>/', views.add_discount_to_item),
	# path('add_discount_to_item/<int:pk>', views.add_discount_to_item),
	path('add_complex_rule_to_store_1/<slug:rule_id1>/<int:store_id>/<slug:which_button>',
	     views.add_complex_rule_to_store_1),
	path('add_complex_rule_to_store_1/<slug:rule_id1>/<int:store_id>/<slug:which_button>/',
	     views.add_complex_rule_to_store_1),
	path('add_complex_rule_to_store_2/<slug:rule_id_before>/<int:store_id>/<slug:which_button>',
	     views.add_complex_rule_to_store_2),
	path('add_complex_rule_to_store_2/<slug:rule_id_before>/<int:store_id>/<slug:which_button>/',
	     views.add_complex_rule_to_store_2),

	path('add_base_rule_to_item/<int:pk>/<slug:which_button>', views.add_base_rule_to_item),
	path('add_base_rule_to_item/<int:pk>/<slug:which_button>/', views.add_base_rule_to_item),
	path('add_complex_rule_to_item_1/<slug:rule_id1>/<int:item_id>/<slug:which_button>',
	     views.add_complex_rule_to_item_1),
	path('add_complex_rule_to_item_1/<slug:rule_id1>/<int:item_id>/<slug:which_button>/',
	     views.add_complex_rule_to_item_1),
	path('add_complex_rule_to_item_2/<slug:rule_id_before>/<int:item_id>/<slug:which_button>',
	     views.add_complex_rule_to_item_2),
	path('add_complex_rule_to_item_2/<slug:rule_id_before>/<int:item_id>/<slug:which_button>/',
	     views.add_complex_rule_to_item_2),
	path('remove_rule_from_store/<int:pk>/<int:type>/<int:store>', views.remove_rule_from_store),
	path('remove_rule_from_item/<int:pk>/<int:type>/<int:item>', views.remove_rule_from_item),
	path('delete_item/<int:pk>/', views.ItemDelete.as_view(success_url="/login_redirect")),
	path('delete_owner/<int:pk_owner>/<int:pk_store>', views.delete_owner),
]


