from django.contrib import admin
from django.urls import path
from avatar.views import personagens

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', personagens, name='personagens'),
]