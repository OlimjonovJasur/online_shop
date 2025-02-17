from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

import user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apelsin/', include('shop.urls'), name='shop'),
    path('user/', include('user.urls'), name='user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
