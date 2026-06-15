from django import forms
from .models import Comment, ContactMessage, Post, Profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']




class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'title',
            'image',
            'body'
        ]

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile

        fields = [
            'bio',
            'profile_picture',
        ]

class ContactForm(forms.ModelForm):

    class Meta:

        model = ContactMessage

        fields = [
            'name',
            'email',
            'message'
        ]