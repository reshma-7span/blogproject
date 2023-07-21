from django import forms
from .models import Blog, Comment, User
from django.contrib.auth.forms import UserCreationForm


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')
