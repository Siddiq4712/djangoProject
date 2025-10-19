from rest_framework import serializers
from books.models import Book
from django.contrib.auth.models import User
from borrow.models import BorrowedBook  # ADD THIS IMPORT

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'description', 'cover_image', 'published_date']  # RE-ADD cover_image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ADD THIS NEW SERIALIZER
class BorrowedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BorrowedBook
        fields = [
            'id',
            'book',
            'book_title',
            'book_author',
            'user',
            'user_username',
            'borrow_date',
            'due_date',
            'return_date',
            'status',
            'is_overdue'
        ]
        read_only_fields = ['user', 'book', 'status']  # User and book set internally, status derived
