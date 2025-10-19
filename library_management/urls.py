from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('borrow/', include('borrow.urls')),        # ADD THIS LINE
    # path('notifications/', include('notifications.urls')), # Notifications won't have direct user URLs
    path('analytics/', include('analytics.urls')), # ADD THIS LINE
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url='/users/login/', permanent=False), name='home'), # Redirect root to login page
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # RE-ADD THIS
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
