from django.contrib import admin
from .models import Comment, Category


admin.site.register(Comment)
admin.site.register(Category)
