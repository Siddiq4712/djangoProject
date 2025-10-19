# utils/helpers.py
# This file is for generic utility functions that might be shared across apps.

import qrcode
import qrcode.image.svg
from io import BytesIO
from django.utils.safestring import mark_safe

def generate_qr_code_svg(data, box_size=5):
    """
    Generates an SVG string for a QR code from the given data.
    """
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(data, image_factory=factory, box_size=box_size)
    stream = BytesIO()
    img.save(stream)
    return mark_safe(stream.getvalue().decode('utf-8'))

# Example recommendation logic placeholder if not in views:
def get_recommendations_for_book(book, num_recommendations=5):
    """
    Provides simple book recommendations based on author or recent additions.
    """
    # 1. Books by the same author (excluding the current book)
    recommended_books = book.objects.filter(author=book.author).exclude(pk=book.pk)

    if recommended_books.count() < num_recommendations:
        # Fill with other recently added books if not enough by same author
        remaining_count = num_recommendations - recommended_books.count()
        recent_books = Book.objects.exclude(pk=book.pk).exclude(id__in=recommended_books.values_list('id', flat=True)).order_by('-published_date')[:remaining_count]
        recommended_books = list(recommended_books) + list(recent_books)

    return recommended_books[:num_recommendations]

