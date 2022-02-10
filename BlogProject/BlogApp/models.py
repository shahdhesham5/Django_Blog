from django.db import models
from django.contrib.auth.models import User #User model to access users and admins
from django.utils import timezone
# import datetime
# from django.utils.timezone import now
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    content = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)
    # datetime = models.DateTimeField(default=datetime.datetime.now)
    # date = models.DateTimeField(auto_now_add=True, blank=True)
    # created_date = models.DateTimeField(default=now, editable=False)
    post_img= models.ImageField(upload_to='images/', null=True)
    
    def __str__(self):
        return self.title      

    # class Meta:
    #     ordering = ['-created_date']

# class order (models.Model):
#     post = models.ForeignKey(Post, models.DO_NOTHING)
#     class Meta:
#         ordering = ['post__title']

  


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_info = models.CharField(max_length=250)
    # created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_info


class Category(models.Model):
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.text
