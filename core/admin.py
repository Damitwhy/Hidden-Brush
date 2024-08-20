from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Comment, Image, Like

admin.site.register(User)
admin.site.register(User, UserAdmin)

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_id', 'text', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'likes_count', 'liked_by')
    search_fields = ('user__username', 'title', 'description')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    fields = ('user', 'image', 'title', 'description', 'created_at')
    readonly_fields = ('created_at',)

    def likes_count(self, obj):
        return obj.get_likes_count()
    likes_count.short_description = 'Likes Count'

    def liked_by(self, obj):
        return ", ".join([like.user.username for like in obj.like_set.all()])
    liked_by.short_description = 'Liked By'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username', 'image__title')
    list_filter = ('user', 'image')
    ordering = ('user', 'image')