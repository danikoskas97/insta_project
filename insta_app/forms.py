from django import forms 
from django.core import validators
from django.contrib.auth.models import User
from insta_app.models import Profile , Post , Comment

class UserForm(forms.ModelForm):
  password = forms.CharField(widget= forms.PasswordInput)
  class Meta:
    model = User 
    help_texts = { 'username': None}
    fields = { 'username', 'email', 'password' }

class UserProfileInfoForm(forms.ModelForm):
  class Meta:
    model = Profile
    help_texts = { 'username': None}
    fields = ('photo','bio')
    
class LoginForm(forms.ModelForm):
  class Meta:
    model   = User
    fields  = ['username','password']
    help_texts = { 'username': None}
    widgets = {
      'username': forms.TextInput(attrs={
        'id': 'login-username',
        'placeholder': 'username',
        'required': True
      }),
      'password': forms.PasswordInput(attrs={
        'id': 'login-password',
        'placeholder': 'password',
        'required': True
      }),
    } 
class PostFrom(forms.ModelForm):
  class Meta:
    model = Post
    help_texts = { 'username': None}
    fields = ('photo','text',)


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    help_texts = { 'username': None}
    fields = ('text',)    



    


    