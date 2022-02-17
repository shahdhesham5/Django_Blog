from django.contrib import admin
from .models import Comment, Category, Message,Post ,Fwords, Tag


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Fwords)
admin.site.register(Message)