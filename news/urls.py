from django.urls import path
from .views import news_feed, like_post, add_comment

app_name = 'news'

urlpatterns = [
    path('', news_feed, name='news_feed'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
]
