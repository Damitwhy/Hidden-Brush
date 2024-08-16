from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Comment, Image
from .forms import CommentForm, ImageForm
from django.conf import settings
import os



from django.shortcuts import render
from django.urls import reverse
import os
from django.conf import settings

def gallery(request):
    return render(request, 'core/gallery.html')


def home(request):
    # Renders the home page template
    return render(request, 'core/home.html')


@login_required
def image_detail(request, image_id):
    # Get all comments on the image, excluding the logged-in user's comments
    other_comments = Comment.objects.filter(image_id=image_id).exclude(user=request.user).order_by('created_at')

    #Get the logged-in user's comments
    user_comments = Comment.objects.filter(image_id=image_id, user=request.user).order_by('created_at')

    #Combine the comments
    comments = list(other_comments) + list(user_comments)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image_id = image_id
            comment.save()
            return redirect('image_detail', image_id=image_id)
    else:
        form = CommentForm()
    return render(request, 'image_detail.html', {'image_id': image_id, 'comments': comments, 'form': form})

# CRUD views for Image model
@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('gallery')
    else:
        form = ImageForm()
    return render(request, 'core/add_image.html', {'form': form})

@login_required
def update_image(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = ImageForm(instance=image)
    return render(request, 'core/update_image.html', {'form': form})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)
    if request.method == 'POST':
        image.delete()
        return redirect('gallery')
    return render(request, 'core/delete_image.html', {'image': image})