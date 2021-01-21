from django.forms import ModelForm
from .models import Profile, User, Post

from django.contrib.auth.forms import UserCreationForm, forms

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['current_city']

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


        