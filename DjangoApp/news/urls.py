from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash = False)
router.register(r'news', views.GenericNewsViewSet, 'news')

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('<int:pk>/', views.news_detail, name='news_detail'),
#     path('news',views.GenericNewsViewSet.as_view({'get': 'get_all'})),
#     path('news', views.GenericNewsViewSet.as_view({'post': 'post_news'})),
#     path('news/<int:pk>', views.GenericNewsViewSet.as_view({'get': 'get_one'})),
#     path('news/<int:pk>', views.GenericNewsViewSet.as_view({'patch': 'update_news'})),
#     path('news/<int:pk>', views.GenericNewsViewSet.as_view({'delete': 'delete_news'})),
    
# ]

urlpatterns = router.urls

