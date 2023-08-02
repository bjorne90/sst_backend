from django.contrib import admin
from .models import News, Like, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_like_count', 'get_comment_count')

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    get_like_count.short_description = 'Likes'
    get_comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'timestamp']
    list_filter = ['timestamp']
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()

    delete_selected.short_description = 'Delete selected comments'


