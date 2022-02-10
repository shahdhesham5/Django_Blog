from unicodedata import name
from django.db import models
from django.contrib.auth.models import User #User model to access users and admins

class Comment(models.Model):
    comment_info = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_info


