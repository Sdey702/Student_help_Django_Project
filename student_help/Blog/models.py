from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image

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
    
    def save(self, *args, **kwargs):
        super(BlogPost, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 800 or img.width > 2000:
            output_size = (600, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ['-date_posted']

    



class AddPost(models.Model):
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=400)
    content = models.TextField()