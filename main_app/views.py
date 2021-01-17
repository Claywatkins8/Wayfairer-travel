from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Profile, User, Post, City 
from .forms import Profile_Form, NewUserForm, Post_Form
# Once we have routes that need locking we can put in @login_required

# Define the home view


def home(request):
    error_message = ''
    if request.method == 'POST':
        signup_form = NewUserForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('profile/')
        else:
            error_message = 'Invalid signup, please try again!'
            
    signup_form = NewUserForm()
    login_form = AuthenticationForm()
    context = {'signup_form': signup_form,
               'error_message': error_message, 'login_form': login_form}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def profile(request):
    if request.method == 'POST':
        profile_form = Profile_Form(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            print(profile_form)
            profile.save()
            return redirect('profile')

    user = User.objects.get(id = request.user.id) 
    if Profile.objects.filter(user_id = request.user.id):
        profile = Profile.objects.get(user_id = request.user.id)
    else:
        profile = ""
    profile_form = Profile_Form()
    posts = Post.objects.filter(user=request.user)
    context = {'profile': profile, 'profile_form': profile_form, 'user': user, 'posts': posts}
    return render(request, 'profile.html', context)

def profile_edit(request):
    profile = Profile.objects.get(user_id = request.user.id)
    user = User.objects.get(id = request.user.id)
    if request.method == 'POST':
        profile_form = Profile_Form(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

    profile_form = Profile_Form(instance=profile)
    user_form = NewUserForm(instance=user)
    context = {'profile_form': profile_form, 'profile': profile, 'user_form': user_form, 'user': user}
    return render(request, 'profiles/edit.html', context)

def post_create(request):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city_id = 1 #write a query that will pull the current city from profile
            new_post.save()
            return redirect('profile')
    
    post_form = Post_Form()
    context = {'post_form': post_form, }
    return render(request, 'posts/create.html', context)

def post_show(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'posts/show.html', context)

def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post_show', post_id=post.id)

    post_form = Post_Form(instance=post)
    context = {'post_form': post_form, 'post': post}
    return render(request, 'posts/edit.html', context)

def post_delete(request, post_id):
    Post.objects.get(id = post_id).delete()
    return redirect('profile')



# REVIEW: Do not need page anymore? in modal?
# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             # We are going to return redirect to home but will change this later
#             return redirect('')
#         else:
#             error_message = 'Invalid signup, please try again!'
#     form = UserCreationForm()
#     context = {'form':form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)
