from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('<slug:slug>/',views.detail,name='detail'),
]