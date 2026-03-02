from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone


from .resource import list_category
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    heading = models.CharField(max_length=30)
    
    content = RichTextUploadingField(verbose_name='Текст новости')  # обратите внимание

    date_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name = 'post')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)  # добавить, можно null для существующих

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    def __str__(self):
        return f'{self.heading} - {self.content}'
    
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name = 'author_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # новое поле

    def __str__(self):
        return f'{self.text}'
    
class Category(models.Model):
    name = models.CharField(max_length=3, choices=list_category)

    def __str__(self):
        return dict(list_category).get(self.name, self.name)

class Appointment(models.Model):
    date = models.DateField(
        default=timezone.now,
    )
    user_site = models.CharField(
        max_length=200
    )
    message = models.TextField()
 
    def __str__(self):
        return f'{self.user_site}: {self.message}'
    

# class OneTimeCode(models.Model):
#     code = models.CharField(max_length=7)
    
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')  # чтобы пользователь не мог подписаться на одну категорию дважды