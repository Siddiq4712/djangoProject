from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

def _send_email(subject, html_message, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL):
    """Helper to send an email with HTML content."""
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def send_welcome_email(user):
    """Sends a welcome email upon user registration."""
    subject = 'Welcome to the Library Management System!'
    context = {'user': user}
    html_message = render_to_string('notifications/welcome_email.html', context)
    _send_email(subject, html_message, [user.email])

def send_borrow_confirmation_email(user, borrowed_item):
    """Sends an email to the user confirming a book borrow."""
    subject = f'Book Borrowed: "{borrowed_item.book.title}"'
    context = {'user': user, 'borrowed_item': borrowed_item}
    html_message = render_to_string('notifications/borrow_confirmation_email.html', context)
    _send_email(subject, html_message, [user.email])

def send_return_confirmation_email(user, borrowed_item):
    """Sends an email to the user confirming a book return."""
    subject = f'Book Returned: "{borrowed_item.book.title}"'
    context = {'user': user, 'borrowed_item': borrowed_item}
    html_message = render_to_string('notifications/return_confirmation_email.html', context)
    _send_email(subject, html_message, [user.email])

def send_admin_issue_notification_email(user, borrowed_item):
    """Sends an email to admins when a book is issued."""
    # This assumes there's at least one admin with an email configured
    admin_emails = [admin.email for admin in User.objects.filter(is_staff=True, is_superuser=True, email__isnull=False)]
    if not admin_emails:
        return # No admin emails to send to

    subject = f'New Book Issue: "{borrowed_item.book.title}" by {user.username}'
    context = {'user': user, 'borrowed_item': borrowed_item}
    html_message = render_to_string('notifications/admin_issue_notification_email.html', context)
    _send_email(subject, html_message, admin_emails)

def send_due_reminders():
    """Sends reminders for books due soon or overdue."""
    from borrow.models import BorrowedBook # Import here to avoid circular dependency

    # Get books due tomorrow
    tomorrow = timezone.now() + timedelta(days=1)
    due_tomorrow_items = BorrowedBook.objects.filter(
        due_date__date=tomorrow.date(),
        return_date__isnull=True
    ).select_related('user', 'book')

    for item in due_tomorrow_items:
        subject = f'Reminder: Your book "{item.book.title}" is due tomorrow!'
        context = {'user': item.user, 'borrowed_item': item, 'type': 'due_soon'}
        html_message = render_to_string('notifications/reminder_email.html', context)
        _send_email(subject, html_message, [item.user.email])

    # Get overdue books (not returned yet)
    overdue_items = BorrowedBook.objects.filter(
        due_date__lt=timezone.now(),
        return_date__isnull=True
    ).select_related('user', 'book')

    for item in overdue_items:
        subject = f'Overdue Alert: Your book "{item.book.title}" is overdue!'
        context = {'user': item.user, 'borrowed_item': item, 'type': 'overdue'}
        html_message = render_to_string('notifications/reminder_email.html', context)
        _send_email(subject, html_message, [item.user.email])

    # Optional: Send admin summary of overdue books
    if overdue_items.exists():
        admin_emails = [admin.email for admin in User.objects.filter(is_staff=True, is_superuser=True, email__isnull=False)]
        if admin_emails:
            subject = f'Overdue Books Summary: {overdue_items.count()} books currently overdue.'
            context = {'overdue_items': overdue_items, 'type': 'admin_summary'}
            html_message = render_to_string('notifications/admin_overdue_summary_email.html', context)
            _send_email(subject, html_message, admin_emails)


# MODIFICATION TO USERS APP TO SEND WELCOME EMAIL
# This is a backend change, not a new file.
# In users/views.py, inside the register view, after form.save():
# from notifications.utils import send_welcome_email
# ...
# user = form.save()
# send_welcome_email(user) # ADD THIS LINE
# messages.success(request, f'Account created for {user.username}! You can now log in.')
