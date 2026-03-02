from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.mixins import LoginRequiredMixin



class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст новости')
    class Meta:
        model = Post
        fields = [
            'heading',
            'content',
            'category',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }