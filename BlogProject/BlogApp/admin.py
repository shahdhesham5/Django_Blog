from django.contrib import admin
from .models import Comment, Category, Post


# admin.site.register(Post)
# admin.site.register(order)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ["title","content","created_on","post_img"]

    list_display_links = ["title","created_on"]

    search_fields = ["title"]

    list_filter = ["created_on"]

    class Meta:
        model = Post
admin.site.register(Category)
admin.site.register(Post)
