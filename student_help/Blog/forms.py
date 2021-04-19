from django import forms
from .models import AddPost

class AddPostForm(forms.ModelForm):

    class Meta:
        model = AddPost
        fields = ['title','intro','content']

        