from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryView.as_view()),
    path('posts/', PostView.as_view()),
    path('delete/<pk>/', PostView.as_view()),
]