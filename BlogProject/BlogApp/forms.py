from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Category, Comment
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('__all__')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','comment_info']

#a form to add a category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)
