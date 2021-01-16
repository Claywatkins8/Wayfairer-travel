from django.forms import ModelForm
from .models import Profile, User, Post

from django.contrib.auth.forms import UserCreationForm, forms

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['current_city']

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=75)
    last_name = forms.CharField(max_length=75)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


        