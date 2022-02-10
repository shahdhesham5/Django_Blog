from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  
from .models import Comment
from django import forms
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["user","title","content","datetime","post_img"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','comment_info']


