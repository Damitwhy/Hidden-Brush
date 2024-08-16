from django import forms
from .models import Comment, Image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description']

