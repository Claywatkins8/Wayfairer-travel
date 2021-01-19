from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Profile, User, Post, City, Photo
from .forms import Profile_Form, NewUserForm, Post_Form
# AWS IMPORTS
import boto3
import uuid
# AWS "Constants"
S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'wayfarer-app1'
# Once we have routes that need locking we can put in @login_required

# Define the home views

def city_show(request, city_id):
    city = City.objects.get(id=city_id)
    posts = Post.objects.all()
    context = {'posts': posts, 'city': city}
    return render(request, 'cities/city.html', context)


def home(request):
    error_message = ''
    if request.method == 'POST':
        signup_form = NewUserForm(request.POST)
        username_form = request.POST['username']
        email_form = request.POST['email']
        city = request.POST['current_city']
        if User.objects.filter(username=username_form).exists():
            context = {'error': 'Username is already taken'}
            return render(request, 'home.html', context)
        else:
            if User.objects.filter(email=email_form).exists():
                context = {'error': 'That email is already taken'}
                return render(request, 'home.html', context)
            else:
                if signup_form.is_valid():
                    user = signup_form.save()
                    user.profile.current_city = city
                    user.save()
                    login(request, user)
                    return redirect('profile/')
                else:
                    context = {'error': 'Invalid signup, please try again!'}
                    return render(request, 'home.html', context)

    profile_form = Profile_Form()
    signup_form = NewUserForm()
    login_form = AuthenticationForm()
    context = {'signup_form': signup_form,
               'login_form': login_form, 'profile_form': profile_form}
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

    user = User.objects.get(id=request.user.id)
    if Profile.objects.filter(user_id=request.user.id):
        profile = Profile.objects.get(user_id=request.user.id)
    else:
        profile = ""
    profile_form = Profile_Form()
    posts = Post.objects.filter(user=request.user)
    context = {'profile': profile, 'profile_form': profile_form,
               'user': user, 'posts': posts}
    return render(request, 'profile.html', context)


def profile_edit(request):
    profile = Profile.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        print("I am in the post")
        city = request.POST['current_city']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user.last_name = last_name
        user.first_name = first_name
        user.profile.current_city = city
        user.save()
        return redirect('profile')

    profile_form = Profile_Form(instance=profile)
    user_form = NewUserForm(instance=user)
    context = {'profile_form': profile_form, 'user_form': user_form, 'user': user, 'profile': profile}
    return render(request, 'profiles/edit.html', context)


def post_create(request):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city_id = 1  # write a query that will pull the current city from profile
            new_post.save()
            return redirect('profile')

    post_form = Post_Form()
    context = {'post_form': post_form, }
    return render(request, 'posts/create.html', context)


def post_show(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=post.user_id)
    # if Profile.objects.filter(user_id=request.user.id):
        # profile = Profile.objects.get(user_id=request.user.id)


    context = {'post': post, 'user':user }
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
    Post.objects.get(id=post_id).delete()
    return redirect('profile')

# AWS ADD PHOTO


def add_photo(request, profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, profile_id=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')


def photo_delete(request, photo_id):
    Photo.objects.get(id=photo_id).delete()
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
