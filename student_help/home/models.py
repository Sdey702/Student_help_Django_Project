from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from PIL import Image
from embed_video.fields import EmbedVideoField

class Content(models.Model):

    tagchoices = [
       ('array','array'),
       ('linklist','linklist'),
       ('stack','stack'),
       ('string','string'),
       ('matrix','matrix'),
       ('searching & sorting','searching & sorting'),
       ('binary tree','binary tree'),
       ('binary search tree','binary search tree'),
       ('greedy','greedy'),
       ('backtracking','backtracking'),
       ('heap','heap'),
       ('graph','graph'),
       ('tire','tire'),
       ('dynamic programing','dynamic programing'),
       ('bit manipulation','bit manipulation'),

    ]
    


    tag = models.CharField(max_length=25,default= 'add a tag',choices=tagchoices)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    exmple = models.TextField(default='ex')
    intro = models.TextField(default = 'abc')
    code = models.TextField(default = 'abc')
    body = models.TextField(default = 'abc')
    video = EmbedVideoField(blank=True)
    comments = GenericRelation(Comment)
    date_added = models.DateTimeField(auto_now=True)

    
    



# save the record with title name
    def __str__(self):
        return 'New record:'+self.title 
    


# profile

class Userprofile(models.Model):
    user = models.OneToOneField(User, null=True, related_name='Userprofile', blank=True, on_delete=models.CASCADE)
    image = models.ImageField(default='linux2.png', upload_to='profile_pics')
    phone = models.CharField(default='1234567890',max_length=10)

    def __str__(self):
        return f'{self.user.username} Userprofile'

    def save(self, *args, **kwargs):
        super(Userprofile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def get_absolute_url(self):
        return reverse('post:postdetail', kwargs={'slug': self.slug})

# comment


# hi
# class Comment models.Model):
#     author = models.CharField(help_text="Enter your name",max_length=100)
#     comment_field = models.CharField(max_length=500,help_text="Write your comment")
#     date_created = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey('Content', related_name="comments" ,on_delete=models.CASCADE)
#     reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="replies", null=True)

#     def __str__(self):
#         return self.author

#     class Meta:
#         ordering = ['date_created']