from django.shortcuts import render,redirect,reverse
from .models import Content,Userprofile 
from django.contrib import messages 
from django.contrib.auth.models import User       
from django.contrib.auth import authenticate,logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
import sys
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView


def index(request):
    return render(request,'home/home.html')   



def ds(request):
    #get all posts
    posts = Content.objects.all()
    #pageing
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request,'home/DS-array.html',{'users': users})


# # description of question
# def desc(request, pk):
#     posts = Content.objects.get(id=pk)
#     print('..................============',posts.id)
#     return render(request, 'home/descripe.html',{'post': posts})


class PostDetailView(DetailView):
    model = Content
    template_name = 'home/descripe.html'


def qus(request,tag):
    posts = Content.objects.filter(tag__iexact=tag)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request,'home/DS-array.html',{'users': users})


    
def about(request):
    return render(request,'home/about.html')

def contact(request):
    return render(request,'home/contact.html')


# new user registation
def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'home/signup.html', {'form': form})


   
    
    

def login(request):
    
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        password=request.POST['password']

        # print(username,password)
        user = authenticate(username = username, password = password)
        # print(user)
        if user is not None :
            auth_login(request, user)
            messages.success(request,f'Welcome {username}!')
            return redirect('index')
        else :
            messages.warning(request,'check you username and password')
            return redirect('index')
     
    else:
        return HttpResponse("404 - Not found")



def logout(request):
    if request.method=="POST":
        auth_logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('index')




@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.Userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.Userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'home/profile.html',context)



       
