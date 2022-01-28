
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import sys

TESTING = sys.argv[1:2] == ['test']
MIGRATION = sys.argv[1:2] == ['makemigrations'] or sys.argv[1:2] == ['migrate']
if not TESTING and not MIGRATION:
    urlpatterns[1:1] = path('', include('blog.urls'))
