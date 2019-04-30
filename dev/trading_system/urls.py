from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path(r'^item_page/(?P<id>\d+)/$', views.item),

	path('actionUrl/', views.search),
	path('login_redirect', views.login_redirect),
]
