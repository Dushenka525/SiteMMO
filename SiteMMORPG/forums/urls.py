from django.urls import path, include
from .views import *


urlpatterns = [
    path('', PostsList.as_view(), name = 'posts'),
    path('<int:pk>/', PostDetail.as_view(),name='post_detail'),
    path('create/', PostCreate.as_view(), name ='create_post'),
    path('update/<int:pk>/', PostUpdate.as_view(), name ='update_post'),
    path('delete/<int:pk>/', PostDelete.as_view(), name ='delete_post'),
    path('my-comments/', my_comments, name='my_comments'),
    path('subscribe/', toggle_subscription, name='toggle_subscription'),





    # path(),  # для загрузки изображений
]