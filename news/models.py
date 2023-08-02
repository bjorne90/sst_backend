from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='commented_posts')
    image = CloudinaryField('image', blank=True, null=True) 

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('News', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
