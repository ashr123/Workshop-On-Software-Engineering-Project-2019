from django.urls import path
from . import views

urlpatterns = [
	path('add_store/', views.add_store),
	path('view_details/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
	#	path('delete/<int:pk>/', views.ArticleDelete.as_view()),
	#	path('update/<int:pk>', views.ArticleUpdate.as_view()),
	path('add_store/submit/', views.submit_open_store),
	path('home_page_owner/', views.StoreListView.as_view(), name='store-list'),
]
