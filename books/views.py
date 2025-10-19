# books/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, OuterRef, Exists

from .models import Book
from .forms import BookForm
from borrow.models import BorrowedBook

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    ordering = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Annotate each book with whether it is currently borrowed
        currently_borrowed_subquery = BorrowedBook.objects.filter(
            book=OuterRef('pk'),
            return_date__isnull=True
        )

        queryset = queryset.annotate(
            is_borrowed=Exists(currently_borrowed_subquery)
        )

        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        # Filter by availability
        availability = self.request.GET.get('availability')
        if availability == 'available':
            queryset = queryset.filter(is_borrowed=False)
        elif availability == 'borrowed':
            queryset = queryset.filter(is_borrowed=True)

        # Sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by == 'author':
                queryset = queryset.order_by('author')
            elif sort_by == 'published_date_desc':
                queryset = queryset.order_by('-published_date')
            elif sort_by == 'title_desc':
                queryset = queryset.order_by('-title')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['availability'] = self.request.GET.get('availability', '')
        context['sort_by'] = self.request.GET.get('sort_by', 'title')
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # Check if the book is currently borrowed
        is_borrowed_by_current_user = False
        is_currently_borrowed_by_anyone = BorrowedBook.objects.filter(
            book=book, return_date__isnull=True
        ).exists()
        
        if self.request.user.is_authenticated:
            is_borrowed_by_current_user = BorrowedBook.objects.filter(
                book=book, user=self.request.user, return_date__isnull=True
            ).exists()

        context['is_borrowed_by_current_user'] = is_borrowed_by_current_user
        context['is_currently_borrowed_by_anyone'] = is_currently_borrowed_by_anyone

        # Simple AI-Powered Recommendations
        same_author_books = Book.objects.filter(author=book.author).exclude(pk=book.pk)
        if not same_author_books.exists():
            recommended_books = Book.objects.exclude(pk=book.pk).order_by('-published_date')[:5]
        else:
            recommended_books = same_author_books.order_by('?')[:5]

        context['recommended_books'] = recommended_books
        return context


class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Book added successfully!')
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    context_object_name = 'book'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Book deleted successfully!')
        return super().form_valid(form)
