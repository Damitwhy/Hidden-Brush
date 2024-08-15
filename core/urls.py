from django.urls import path

from . import views
from .views import home

urlpatterns = [('', views.home.as_view(), name='home'),
      
]