from django import forms
from .models import Comment, Image
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Point to your custom User model
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please choose another.")
        return email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description']
