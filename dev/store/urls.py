from django.urls import path
from . import views

urlpatterns = [
	path('add_store/', views.add_store),
	path('add_item/<int:pk>', views.add_item),
	path('add_item_2/', views.AddItemToStore.as_view()),
	path('view_details/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
	path('delete/<int:pk>/', views.StoreDelete.as_view()),
	path('add_item_to_store/<int:pk>/', views.AddItemToStore.as_view()),
	path('buy_item/<int:pk>/', views.buy_item),
	path('update/<int:pk>', views.StoreUpdate.as_view()),
	path('add_store/submit/', views.submit_open_store),
	path('home_page_owner/', views.StoreListView.as_view(), name='store-list', ),
	path('itemAddedSuccessfully/<int:pk>', views.itemAddedSucceffuly, name='item-detail', ),
]
