# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import PostImages, Post, Comment

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(label="Body", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostImagesInline(admin.TabularInline):
    list_display = ('caption', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('caption',)}
    model = PostImages
    exta = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [PostImagesInline, ]
    form = PostAdminForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'content_object', 'timestamp', 'active')
    list_filter = ('active', 'timestamp')
    search_fields = ('user', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
