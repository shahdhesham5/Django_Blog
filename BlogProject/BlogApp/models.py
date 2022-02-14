from django.db import models
from django.contrib.auth.models import User #User model to access users and admins
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category

class Tag(models.Model):
    tag_item = models.CharField(max_length=20, default=None)
    def __str__(self):
        return self.tag_item   
class Fwords(models.Model):
    fword = models.CharField(max_length=20)
    def __str__(self):
        return self.fword

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    content = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=timezone.now)
    post_img= models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag ,related_name='tags', blank=True)
    likes = models.ManyToManyField(User , related_name='blog_like')
    dislikes = models.ManyToManyField(User , related_name='blog_dislike')

    def total_likes(self):
        return self.likes.count()
        
    def total_dislikes(self):
        return self.dislikes.count()
        
    def __str__(self):
        return self.title      

    class Meta:
        ordering = ('-created_on',)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_info = models.CharField(max_length=250)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_info

class Subscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)