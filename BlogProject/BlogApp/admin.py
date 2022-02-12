from django.contrib import admin
from .models import Comment, Category,Post,Tag


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
