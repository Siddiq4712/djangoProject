from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser  # ADD IsAdminUser
from books.models import Book
from django.contrib.auth.models import User
from borrow.models import BorrowedBook  # ADD THIS IMPORT
from .serializers import BookSerializer, UserSerializer, BorrowedBookSerializer  # UPDATE THIS IMPORT
from rest_framework import serializers  # Required for ValidationError

class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Anyone can list books. For creation, consider IsAuthenticated or IsAdminUser

    def perform_create(self, serializer):  # Ensure only staff can create
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise serializers.ValidationError({"detail": "You do not have permission to perform this action."})

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Anyone can view book details. For update/delete, consider IsAdminUser

    def get_permissions(self):
        # Allow anyone to GET (retrieve), but only staff to PUT/PATCH (update) or DELETE
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list users
    # For security, you might want to restrict this further to IsAdminUser

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view user details
    # A user should only be able to view their own details unless they are admin
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

# ADD THESE NEW API VIEWS
class BorrowedBookListAPIView(generics.ListAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAdminUser]  # Only admins can view all borrowed books

class UserBorrowedBooksAPIView(generics.ListAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]  # Authenticated users can view their own borrowed books

    def get_queryset(self):
        # Filter borrowed books to only show those of the authenticated user
        return BorrowedBook.objects.filter(user=self.request.user).order_by('-borrow_date')
