from django.urls import path
from core.views import home
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'), 
    path('gallery/', views.gallery, name='gallery'),           
]
      
