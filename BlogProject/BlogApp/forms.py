from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django.contrib.auth.models import User  
from .models import Comment
from django import forms
=======
from django.contrib.auth.models import User
from django import forms
from .models import Category
>>>>>>> c412737e6ea25e813494d9e1b7f467cc49ebfd89
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

<<<<<<< HEAD
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["user","title","content","datetime","post_img"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','comment_info']


=======

#a form to add a category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
>>>>>>> c412737e6ea25e813494d9e1b7f467cc49ebfd89
