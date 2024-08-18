from django.urls import path
from core.views import home, gallery, CustomLoginView, RegisterView, LogoutConfirmView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout-confirm/', LogoutConfirmView.as_view(), name='logout-confirm'),
    path('register/', RegisterView.as_view(), name='register'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('gallery/', views.gallery, name='gallery'),
    # CRUD views for Image model
    path('add/', views.add_image, name='add_image'),
    path('update/<int:image_id>/', views.update_image, name='update_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('toggle_like/<int:image_id>/', views.toggle_like, name='toggle_like'),
]
