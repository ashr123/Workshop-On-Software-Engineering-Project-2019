from django.urls import path
from . import views

urlpatterns = [
	path('add_store/', views.add_store),
	path('view_details/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
	path('delete/<int:pk>/', views.StoreDelete.as_view()),
	path('add_item_to_store/<int:pk>/', views.add_item_to_store),

	path('update/<int:pk>', views.StoreUpdate.as_view()),
	path('add_store/submit/', views.submit_open_store),
	path('home_page_owner/', views.StoreListView.as_view(), name='store-list', ),
]
