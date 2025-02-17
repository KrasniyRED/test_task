from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('news/', views.GenericNewsView.as_view(), name='news'),
    path(
        'news/<int:pk>/', views.GenericNewsView.as_view(), name='news_detailed'
    ),
    path(
        'news/<int:pk>/comments/',
        views.GenericCommentsView.as_view(),
        name='comments',
    ),
    path(
        'news/<int:pk>/comments/<int:comment_pk>/',
        views.GenericCommentsView.as_view(),
        name='comments_detailed',
    ),
]
