from django.urls import path
from core.views import home
from . import views


urlpatterns = [
    path('', views.home, name='home'),               
]
      
