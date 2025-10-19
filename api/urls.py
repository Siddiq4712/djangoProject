from django.urls import path
from .views import (
    BookListAPIView,
    BookDetailAPIView,
    UserListAPIView,
    UserDetailAPIView
)

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='api_book_list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='api_book_detail'),
    path('users/', UserListAPIView.as_view(), name='api_user_list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='api_user_detail'),
]
