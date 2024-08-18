from django.contrib import admin
from .models import User, Comment, Image

admin.site.register(User)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_id', 'text', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    search_fields = ('user__username', 'title', 'description')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    fields = ('user', 'image', 'title', 'description', 'created_at')
    readonly_fields = ('created_at',)

