from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import (
    PostDetailView,
)


urlpatterns = [
path('', views.index, name="index"),
path('blog/',include('Blog.urls')),
path('ds/',views.ds, name="Ds_&_algo"),
path('about/',views.about, name="about"),
path('contact/',views.contact, name="contact"),
path('desc/<int:pk>/', PostDetailView.as_view(),name="desc"),

path('comment/', include('comment.urls')),
path('signup',views.signup, name="singup"),
path('Login',views.login, name="login"),
path('Logout',views.logout, name="logout"),
path('profile',views.profile, name="profile"),
path('accounts/login/',views.index, name="login"),


path('array/',views.qus,{'tag':'array'}, name="array"),
path('stack/',views.qus,{'tag':'stack'}, name="array"),
path('string/',views.qus,{'tag':'string'}, name="string"),
path('matrix/',views.qus,{'tag':'matrix'}, name="matrix"),
path('search&sorting/',views.qus,{ 'tag':'searching & sorting'}, name="search&sorting"),
path('linklist/',views.qus,{'tag':'linklist'}, name="linklist"),
path('binarytree/',views.qus,{'tag':'binary tree'}, name="bt"),
path('binarysearchtree/',views.qus,{'tag':'binary search tree'}, name="bst"),
path('greedy/',views.qus,{'tag':'greedy'}, name="greedy"),
path('backtracking/',views.qus,{'tag':'backtracking'}, name="backtracking"),
path('heap/',views.qus,{'tag':'heap'}, name="heap"),
path('graph/',views.qus,{'tag':'graph'}, name="graph"),
path('tire/',views.qus,{'tag':'tire'}, name="tire"),
path('dynamic/',views.qus,{'tag':'dynamic programing'}, name="dynamic"),
path('bit/',views.qus,{'tag':'bit manipulation'}, name="bit manipulation")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)