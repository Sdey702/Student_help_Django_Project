from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages 
from .models import BlogPost
from home.views import index
from .forms import AddPostForm

# Create your views here.

def bloghome(request):
    post = BlogPost.objects.all()
    return render(request,'blog/bloghome.html',{ 'post':post })


# description of question
def detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    # print('..................============',posts.id)
    return render(request, 'blog/detail.html',{'post': post})

#error
def error(request):
    messages.error(request,'login required to join in comment section')
    return redirect('index')



def addpost(request):
    messages.warning(request,'Your post will veryfi and then added')
    if request.method == 'POST':
        formset = AddPostForm(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request,'Your request has been send')
            return redirect('bloghome')
        else:
            messages.error(request,'Something wrong! Try again')
            return redirect('bloghome')
    else:
        formset = AddPostForm()
    return render(request, 'blog/addpost.html', {'form': formset})