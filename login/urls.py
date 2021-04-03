from django.contrib import admin
from django.urls import path
from .app import login_, home, singup, out, check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', singup),
    path('home', home),
    path('login', login_),
    path('out', out),
    path('check', check)
]
