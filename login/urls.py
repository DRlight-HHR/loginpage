from django.contrib import admin
from django.urls import path
from .app import login_, home, singup, out, check
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', singup),
    path('home', home),
    path('login', login_),
    path('out', out),
    path('check', check)
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
