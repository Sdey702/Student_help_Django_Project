from typing import NoReturn
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Content,Userprofile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
import numpy as np
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

#machinelearning for recomandation
import pandas as pd

df = pd.read_csv('./datamodel/qus.csv')
df.columns = [ x.lower() for x in df.columns ]
df['title']=df['title'].apply(lambda x : x.lower())
df['genre']=df['genre'].apply(lambda x : x.lower())
all_titles = [df['title'][i] for i in range(len(df['title']))]

# print(all_titles)
# def re(str):
#     print(str)

#     li = [0,2,5,3]
#     return li

data = df
# Convert the index into series
indices = pd.Series(data.index, index = data['title'])
# print(indices)
#Converting the book title into vectors and used bigram
tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
tfidf_matrix = tf.fit_transform(data['title'])
#data.set_index('title',inplace=True)
# print(data)

def recommend(title):
    # find gener from title
    genre=data.loc[indices[title],'genre']
    #print(title)
    # Matching the genre with the dataset and reset the index
    Data = df.loc[df['genre'] == genre]
    Data.reset_index(level = 0, inplace = True)

    # Calculating the similarity measures based on Cosine Similarity
    sg = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index corresponding to original_title
    #print(type(title))
    idx = indices[title]
    #print("----------------------",idx)
    # Get the pairwsie similarity scores
    sig = list(enumerate(sg[idx]))
    # Sort the books
    sig = sorted(sig, key=lambda x: x[1], reverse=True)
    # Scores of the 5 most similar books
    sig = sig[1:6]
    # Book indicies
    movie_indices = [i[0] for i in sig]

    # Top 5 book recommendation
    li=[]

    rec = data[['title', 'genre']].iloc[movie_indices]
    for i in rec['title']:
      li.append(i)
    return li


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




class PostDetailView(DetailView):
    model = Content
    template_name = 'home/descripe.html'

    var1 = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a=context["object"]
        stri=str(a)

        stri = stri.lower()
        #self.var1 = re(stri)

        if stri in all_titles :
            # print('yes',stri)
            self.var1=recommend(stri)

        return context



    def get_tags(self):
        tags = self.var1
        return tags




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




# search

def search(request):

    abc = request.GET.get('search')
    # print(abc)
    list=[]
    if abc:
        post=Content.objects.filter(title__icontains=abc)

        for i in range(len(post)):

            list.append(str(post[i]))

    return JsonResponse({'status':200,'data':list})


def search_results(request):

    if request.method == 'POST' :
        question = request.POST['search']
        # print(question)

        posts = Content.objects.filter(title=question)

        # print(Content.objects.filter(title__icontains=question).values())


        if len(posts) == 0:
            return render(request,'home/search.html')

        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 4)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request,'home/DS-array.html',{'users': users})

    return render(request,'home/search.html')






