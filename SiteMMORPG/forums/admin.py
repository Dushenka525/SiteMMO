from django.contrib import admin
from forums.models import Category, Author, Post, Comment
# Register your models here.

from django import forms
from ckeditor.widgets import CKEditorWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Текст новости')
    
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('heading', 'date_time', 'category')

# admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
