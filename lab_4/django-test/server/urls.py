from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', test.as_view())
]
