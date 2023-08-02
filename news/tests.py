from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News


class NewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.news = News.objects.create(title='Test News', content='Lorem ipsum dolor sit amet.')

    def test_news_list_view(self):
        response = self.client.get(reverse('news:news_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_feed.html')

    def test_like_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('news:like_post', args=[self.news.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.news.likes.count(), 1)

        response = self.client.get(reverse('news:like_post', args=[self.news.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.news.likes.count(), 0)

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpassword')
        comment_data = {'comment_content': 'This is a test comment.'}
        response = self.client.post(reverse('news:add_comment', args=[self.news.id]), data=comment_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.news.comments.count(), 1)
        self.assertEqual(self.news.comments.first().content, 'This is a test comment.')

    def test_add_comment_invalid_post_id(self):
        self.client.login(username='testuser', password='testpassword')
        comment_data = {'comment_content': 'This is a test comment.'}
        response = self.client.post(reverse('news:add_comment', args=[999]), data=comment_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.news.comments.count(), 0)
