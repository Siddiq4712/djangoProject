from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from books.models import Book
from .models import BorrowedBook
from notifications.utils import (
    send_borrow_confirmation_email,
    send_return_confirmation_email,
    send_admin_issue_notification_email
)

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Check if the book is already borrowed by anyone
    if BorrowedBook.objects.filter(book=book, return_date__isnull=True).exists():
        messages.error(request, f'"{book.title}" is currently unavailable.')
        return redirect('book_detail', pk=pk)

    # Prevent user from borrowing the same book multiple times simultaneously
    # (Though the above check essentially covers this, it's good to be explicit)
    if BorrowedBook.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
        messages.warning(request, f'You have already borrowed "{book.title}".')
        return redirect('book_detail', pk=pk)

    # Create a new borrowed book entry
    borrowed_item = BorrowedBook.objects.create(
        user=request.user,
        book=book,
    )
    messages.success(request, f'You have successfully borrowed "{book.title}". It is due on {borrowed_item.due_date.strftime("%Y-%m-%d")}.')

    # Send notifications
    send_borrow_confirmation_email(request.user, borrowed_item)
    send_admin_issue_notification_email(request.user, borrowed_item)

    return redirect('borrowed_books_user')

@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Find the active borrowed entry for this user and book
    borrowed_item = get_object_or_404(BorrowedBook, user=request.user, book=book, return_date__isnull=True)

    if request.method == 'POST':
        borrowed_item.return_date = timezone.now()
        borrowed_item.status = 'returned'
        borrowed_item.save()
        messages.success(request, f'You have successfully returned "{book.title}".')

        # Send notifications
        send_return_confirmation_email(request.user, borrowed_item)

        return redirect('borrowed_books_user')
    
    context = {
        'title': 'Return Book',
        'book': book,
        'borrowed_item': borrowed_item
    }
    return render(request, 'borrow/return_book.html', context)


@login_required
def user_borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user).order_by('-borrow_date')
    context = {
        'title': 'My Borrowed Books',
        'borrowed_books': borrowed_books
    }
    return render(request, 'borrow/borrowed_books.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff) # Only staff can view all issued books
def admin_issued_books(request):
    all_issued_books = BorrowedBook.objects.select_related('user', 'book').order_by('-borrow_date')

    # Optional: Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        all_issued_books = all_issued_books.filter(status=status_filter)
    
    # Optional: Filter by overdue
    show_overdue = request.GET.get('overdue')
    if show_overdue == 'true':
        all_issued_books = [item for item in all_issued_books if item.is_overdue()]


    context = {
        'title': 'All Issued Books',
        'all_issued_books': all_issued_books,
        'status_filter': status_filter,
        'show_overdue': show_overdue == 'true'
    }
    return render(request, 'borrow/admin_issued_books.html', context)
