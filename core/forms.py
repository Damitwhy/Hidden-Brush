from django import forms
from .models import Comment, Image
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Point to your custom User model
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_username(self):

        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError("This username is already taken. Please choose another.")

        return username


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description']
