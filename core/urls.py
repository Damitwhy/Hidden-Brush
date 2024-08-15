from django.urls import path
from . import views
from .views import home

path [('', views.home.as_view(), name='home'),
      
]