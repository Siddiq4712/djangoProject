from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils import timezone
from datetime import timedelta

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    
    # Status can be 'active', 'returned', 'overdue'
    status = models.CharField(max_length=20, default='active') 

    class Meta:
        # A book can only be actively borrowed by one user at a time
        unique_together = ('book', 'return_date')
        # If return_date is null, it's considered currently borrowed.
        # This requires a partial unique constraint in a real DB for robustness,
        # but for SQLite it will allow multiple if return_date is null.
        # We'll handle uniqueness check in the view logic.

    def save(self, *args, **kwargs):
        if not self.id: # Only set due_date on initial creation
            self.due_date = timezone.now() + timedelta(days=14) # 14 days due date
        super().save(*args, **kwargs)

    def is_overdue(self):
        return self.due_date < timezone.now() and self.return_date is None

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title} (Due: {self.due_date.strftime("%Y-%m-%d")})'
