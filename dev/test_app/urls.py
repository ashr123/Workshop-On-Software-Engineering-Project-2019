"""dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [
	path('test_Simple_Form/', views.get_name),
	path('test_Simple_Form/your-name/', views.get_name),
	path('test1/thanks/', views.thanks),
	path('test_Complex_Form/', views.get_contact),
	path('test_Complex_Form/contactExample/', views.get_name),
	path('test3/', views.noa),
	path('test_AnotherExample/', views.test4),
	path('test_Like_The_One_Above_But_With_Customized_Html/', views.test5),
	# path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
	path('test_Form_That_Represents_Object_Instance____You_Pass_The_PK_In_ThE_Path_!!!!_/<int:pk>/',
	     views.ArticleDetailView.as_view(), name='article-detail'),
	path('test_Form_That_Represents_Full_Table/', views.ArticleListView.as_view(), name='article-list'),
	path('test_Not_Interesting/', views.ContactView.as_view()),
	path('test_create_form/', views.AuthorCreate.as_view()),
	path('test_update_form/<int:pk>', views.AuthorUpdate.as_view()),
	path('test_delete_form/<int:pk>', views.AuthorDelete.as_view()),
]
