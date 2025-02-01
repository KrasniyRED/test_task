from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('new/', views.news_create, name='news_create'),
    path('<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('<int:pk>/delete/', views.news_delete, name='news_delete'),
]