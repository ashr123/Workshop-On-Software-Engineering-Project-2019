from django.urls import path
from . import views

urlpatterns = [
	path('add_store/', views.add_store),
	path('add_item/<int:pk>', views.add_item),
	path('add_item_2/', views.AddItemToStore.as_view()),
	path('view_details/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
	path('delete/<int:pk>/', views.StoreDelete.as_view(success_url="/login_redirect")),
	path('add_item_to_store/<int:pk>/', views.add_item),
	path('buy_item/<int:pk>/', views.buy_item),
	path('update/<int:pk>', views.StoreUpdate.as_view()),
	path('add_store/submit/', views.submit_open_store),
	#path('home_page_owner/<int:o_id>', views.StoreListView.as_view(), name='store-owner-detail', ),
	path('add_item_to_store/<int:int>/<slug:id>', views.itemAddedSucceffuly, name='item-detail'),
	path('home_page_owner/', views.home_page_owner),
	path('view_store/', views.StoreListView.as_view(), name='store-owner-detail',),
	path('view_item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail',)
]
