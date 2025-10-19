# books/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Ensure each field is separate and correctly spelled
        fields = ['title', 'author', 'isbn', 'description', 'cover_image', 'published_date']  # CORRECTED line
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
