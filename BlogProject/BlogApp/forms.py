from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Category, Comment, Post ,Fwords, Tag
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','post_img','category', 'tag']
        widgets = {
            'content': forms.Textarea(attrs={'name': 'body', 'rows': 10}),}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_info']
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_item']
#a form to add a category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)

#a form to add a Forbidden Word
class FwordsForm(forms.ModelForm):
    class Meta:
        model = Fwords
        fields = ('fword',)

