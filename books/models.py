from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, help_text='13 Character ISBN number')
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True) # Added for completeness

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})
