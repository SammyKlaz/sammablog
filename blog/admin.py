from django.contrib import admin
from .models import (
    Post,
    Comment,
    Profile,
    ContactMessage
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'author',
        'created_at'
    ]

    search_fields = [
        'title',
        'body'
    ]

    list_filter = [
        'created_at'
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'post',
         'body',
        'created_at',
    ]

    search_fields = [
        'user__username',
        'body'
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'user__first_name',
        'user__last_name',
        'is_author',
        'author_request'
    ]

    list_filter = [
        'is_author',
        'author_request'
    ]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'email',
        'created_at'
    ]

    search_fields = [
        'name',
        'email'
    ]