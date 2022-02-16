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
        fields = ['title','post_img','category','content', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'post_img': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tag': forms.SelectMultiple(attrs={'class': 'form-select'})
            }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_info']
        widgets = {
            'comment_info': forms.TextInput(attrs={'class': 'form-control', 'data-role':'tagsinput'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_item']
        widgets = {
            'tag_item': forms.TextInput(attrs={'class': 'form-control', 'data-role':'tagsinput'})
        }
        
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

