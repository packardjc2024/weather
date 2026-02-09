"""
Project level urls. Imports url pages from each app and includes the built in
admin urls page.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system_check.urls')),
    path('', include('home_page.urls')),
    path('docs/', include('docs.urls')),
]

# Conditionally use account based on LOGIN_REQUIRED
if settings.USE_ACCOUNT:
    urlpatterns.append(path('account/', include('account.urls')))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)