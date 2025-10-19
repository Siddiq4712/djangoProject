from django.urls import path
from . import views

urlpatterns = [
    path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('my-books/', views.user_borrowed_books, name='borrowed_books_user'),
    path('admin/issued/', views.admin_issued_books, name='admin_issued_books'),
]
