from django.contrib import admin
from .models import BlogPost,AddPost
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(AddPost)