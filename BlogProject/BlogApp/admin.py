from django.contrib import admin
from .models import Comment, Category,Post


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
