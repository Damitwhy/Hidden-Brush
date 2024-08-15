from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy
# Create your views here.
def home(request):
    # Renders the home page template
    return render(request, 'core/home.html')