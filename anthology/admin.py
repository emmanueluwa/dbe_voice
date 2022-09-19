from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'poet', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'poet']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['poet']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

