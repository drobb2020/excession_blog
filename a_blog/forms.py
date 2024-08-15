from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "content", "post_image", "tags")


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "content", "post_image", "status", "tags")


class PostStatusForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "status")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "content")
