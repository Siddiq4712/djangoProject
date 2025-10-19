from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F, ExpressionWrapper, fields
from django.utils import timezone
from books.models import Book
from borrow.models import BorrowedBook
from django.contrib.auth.models import User
from datetime import timedelta

@login_required
@user_passes_test(lambda u: u.is_staff) # Only staff can access analytics
def analytics_dashboard(request):
    """
    Displays an admin-only dashboard with various library statistics.
    """
    # Total counts
    total_users = User.objects.count()
    total_books = Book.objects.count()
    total_borrowed_records = BorrowedBook.objects.count()
    currently_borrowed_books = BorrowedBook.objects.filter(return_date__isnull=True).count()
    overdue_books_count = BorrowedBook.objects.filter(
        due_date__lt=timezone.now(),
        return_date__isnull=True
    ).count()

    # Most borrowed books (by distinct borrow instances)
    most_borrowed_books = BorrowedBook.objects.values('book__title', 'book__author').annotate(
        borrow_count=Count('book')
    ).order_by('-borrow_count')[:5]

    # Active users (those with active borrows)
    active_borrowers = User.objects.filter(
        borrowed_items__return_date__isnull=True
    ).distinct().count()

    # Borrowing trends (last 30 days - simple version)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    borrow_trends = BorrowedBook.objects.filter(
        borrow_date__gte=last_30_days
    ).annotate(
        day=ExpressionWrapper(F('borrow_date'), output_field=fields.DateField())
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')

    # Prepare data for a simple chart (e.g., for Chart.js in template)
    chart_labels = [entry['day'].strftime('%Y-%m-%d') for entry in borrow_trends]
    chart_data = [entry['count'] for entry in borrow_trends]

    context = {
        'title': 'Analytics Dashboard',
        'total_users': total_users,
        'total_books': total_books,
        'total_borrowed_records': total_borrowed_records,
        'currently_borrowed_books': currently_borrowed_books,
        'overdue_books_count': overdue_books_count,
        'most_borrowed_books': most_borrowed_books,
        'active_borrowers': active_borrowers,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'analytics/dashboard.html', context)
