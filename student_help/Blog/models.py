from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    intro = models.CharField(max_length=400,default='intro')
    image = models.ImageField(blank=True,upload_to='blogpostimg')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title
    
class AddPost(models.Model):
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=400)
    content = models.TextField()