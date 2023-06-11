from django.contrib import admin
from .models import Author, Post, Category, Comment, PostCategory, MyModel

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')