from django.urls import path
from core.views import home, image_detail, gallery
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('image/<str:image_id>/', views.image_detail, name='image_detail'),
    path('gallery/', views.gallery, name='gallery'),           
]
      
