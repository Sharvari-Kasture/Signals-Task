from django.contrib import admin
from .models import Post, BlockedUser

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('author', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked_user')
    search_fields = ('user__username', 'blocked_user__username')

