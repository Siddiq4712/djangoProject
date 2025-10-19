from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # User-related URLs
    path('books/', include('books.urls')), # Book-related URLs
    path('', RedirectView.as_view(url='/books/', permanent=False), name='home'), # Redirect root to book list
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
