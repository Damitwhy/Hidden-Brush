from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from django.conf import settings
import os


from django.shortcuts import render
from django.urls import reverse
import os
from django.conf import settings

def gallery(request):
    image_dir = os.path.join(settings.STATIC_ROOT, 'images')
    if not os.path.exists(image_dir):
        return render(request, 'core/gallery.html', {'images': []})

    images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    image_urls = [
        {
            'name': image,
            'url': reverse('image_detail', kwargs={'image_id': image})
        }
        for image in images
    ]
    return render(request, 'core/gallery.html', {'images': image_urls})
    
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