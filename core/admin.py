from django.contrib import admin
from .models import User, Comment

admin.site.register(User)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_id', 'text', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)