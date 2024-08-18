import os
import json
import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.views.generic.list import ListView
from .forms import CommentForm, ImageForm, CustomUserCreationForm
from .models import Comment, Image, Like
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


def gallery(request):
    images = Image.objects.all()

    for image in images:
        image.is_liked_by_user = image.like_set.filter(user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'core/gallery.html', {'images': images})


def home(request):
    # Renders the home page template
    return render(request, 'core/home.html')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        redirect_to = self.request.GET.get('next')
        logging.info(f"Redirecting to: {redirect_to}")
        if redirect_to:
            return redirect_to
        return reverse_lazy('home')
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully logged in.')
        return response


    #def get_success_url(self, form):
    #   response = super().get_success_url(form)
    #   messages.success(self.request, 'You have successfully logged in.')
    #   return response

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'core/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
            # Re-render the form with error messages if the form is invalid
        return render(request, 'core/register.html', {'form': form})


class LogoutConfirmView(LoginRequiredMixin, View):
    template_name = 'core/logout-confirm.html'

    def get(self, request, *args, **kwargs):
        # Renders the logout confirmation page
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Logs out the user, displays a success message, and redirects to the login page
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect(reverse_lazy('login'))


@login_required
def image_detail(request, image_id):

    # Retrieve the image object
    image = get_object_or_404(Image, id=image_id)

    # Get the Cloudinary URL
    image_url = image.image.url

    # Get all comments on the image, excluding the logged-in user's comments
    other_comments = Comment.objects.filter(image_id=image_id).exclude(
        user=request.user).order_by('created_at')

    # Get the logged-in user's comments
    user_comments = Comment.objects.filter(
        image_id=image_id, user=request.user).order_by('created_at')

    # Combine the comments
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
    # Pass the image_url to the template context
    return render(request, 'core/image_detail.html', {
        'image_id': image_id,
        'image_url': image_url,
        'comments': comments,
        'form': form
    })

@login_required
def toggle_like(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    like, created = Like.objects.get_or_create(user=request.user, image=image)
    
    if not created:
        like.delete()  # Unlike the image if it was already liked
    
    return redirect('gallery')


# CRUD views for Image model
@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, 'Image added successfully.')
            return redirect('gallery')
    else:
        form = ImageForm()
    return render(request, 'core/add_image.html', {'form': form})

@login_required
def update_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image.user != request.user:
        return HttpResponseForbidden("You are not authorized to update this image.")
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image updated successfully.')
            return redirect('gallery')
    else:
        form = ImageForm(instance=image)
    return render(request, 'core/update_image.html', {'form': form, 'image': image})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image.user != request.user:
        return HttpResponseForbidden("You are not authorized to delete this image.")
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully.')
        return redirect('gallery')
    return render(request, 'core/delete_image.html', {'image': image})

@login_required
def toggle_like(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    like, created = Like.objects.get_or_create(user=request.user, image=image)
    
    if not created:
        like.delete()  # Unlike the image if it was already liked
    
    return redirect('gallery')
