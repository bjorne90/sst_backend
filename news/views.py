from django.shortcuts import render, redirect
from .models import News, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


@login_required
def news_feed(request):
    news_items = News.objects.all().order_by('-timestamp')
    return render(request, 'news_feed.html', {'news_items': news_items})

@login_required
def like_post(request, post_id):
    post = News.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        messages.success(request, 'You unliked the post.')
    else:
        post.likes.add(user)
        messages.success(request, 'You liked the post.')

    return redirect(reverse('news:news_feed'))

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = News.objects.get(id=post_id)
        user = request.user
        content = request.POST['comment_content']
        comment = Comment(post=post, user=user, content=content)
        comment.save()
        messages.success(request, 'Your comment was added successfully.')
    return redirect(reverse('news:news_feed'))
