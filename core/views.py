from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from django.conf import settings
import os


def gallery(request):
    return render(request, 'core/gallery.html')


def home(request):
    # Renders the home page template
    return render(request, 'core/home.html')


@login_required
def image_detail(request, image_id):
    comments = Comment.objects.filter(image_id=image_id)
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
