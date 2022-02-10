from unicodedata import name
from django.db import models
from django.contrib.auth.models import User #User model to access users and admins
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    content = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)
    post_img= models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.title      

    class Meta:
        ordering = ('title',)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_info = models.CharField(max_length=250)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_info





