from django.urls import path
from .views import (
    BookListAPIView,
    BookDetailAPIView,
    UserListAPIView,
        UserDetailAPIView,
    BorrowedBookListAPIView,      # ADD THIS
    UserBorrowedBooksAPIView      # ADD THIS
)

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='api_book_list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='api_book_detail'),
    path('users/', UserListAPIView.as_view(), name='api_user_list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='api_user_detail'),
    path('borrowed/', BorrowedBookListAPIView.as_view(), name='api_borrowed_list'), # ADD THIS
    path('my-borrowed/', UserBorrowedBooksAPIView.as_view(), name='api_my_borrowed'), # ADD THIS
]
