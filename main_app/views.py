from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
# Once we have routes that need locking we can put in @login_required

# Define the home view


def home(request):
    error_message = ''
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            # We are going to return redirect to home but will change this later
            return redirect('about/')
        else:
            error_message = 'Invalid signup, please try again!'
    signup_form = UserCreationForm()
    login_form = AuthenticationForm()
    context = {'signup_form': signup_form, 'error_message': error_message, 'login_form': login_form}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


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
