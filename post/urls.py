from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


# urlpatterns = [
#     path('categories/', CategoryView.as_view()),
#     path('posts/', PostView.as_view()),
#     path('delete/<pk>/', PostView.as_view()),
# ]

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<slug:pk>/', PostRetriveView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('tags/', TagListCreateView.as_view()),
    path('', include(router.urls))
]