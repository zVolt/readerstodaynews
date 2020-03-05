# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import (
    MenuItem,
    Media,
    Post,
    PostType,
    MediaType,
    Category,
    Comment,
    UserProfile,
    Source,
    Counter,
)
import datetime


class BaseAdmin(admin.ModelAdmin):
    exclude = ["last_modified_by", "last_modified_on"]

    def save_model(self, request, obj, form, change):
        obj.last_modified_by = request.user
        obj.last_modified_on = datetime.datetime.today()
        super(BaseAdmin, self).save_model(request, obj, form, change)


@admin.register(MenuItem)
class MenuItemAdmin(BaseAdmin):
    list_display = ("name", "url", "menu", "order")


@admin.register(Media)
class MediaAdmin(BaseAdmin):
    list_display = ("image_thumbnail", "title")
    readonly_fields = ["image_thumbnail"]

    def image_thumbnail(self, obj):
        return mark_safe(
            '<img src="{url}" width={width} height={height} />'.format(
                url=obj.image.url, width=50, height=50,
            )
        )


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = (
        "summary",
        "title",
        "like_count",
        "comment_count",
        "last_modified_on",
    )
    search_fields = ("title", "summary")
    list_filter = ("last_modified_on", "last_modified_by", "categories")
    ordering = ["-last_modified_on"]

    def like_count(self, obj):
        return obj.likes.count()

    def comment_count(self, obj):
        return obj.comments.count()


@admin.register(PostType)
class PostTypeAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(MediaType)
class MediaTypeAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ("name", "image_thumbnail")

    def image_thumbnail(self, obj):
        return mark_safe(
            '<img src="{url}" width={width} height={height} />'.format(
                url=obj.image.url, width=50, height=50,
            )
        )


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = (
        "user",
        "content",
    )


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    list_display = (
        "user",
        "interests",
    )

    def interests(self, obj):
        return ", ".join([t.name for t in obj.interested_categories.all()])


@admin.register(Source)
class SourceAdmin(BaseAdmin):
    list_display = (
        "name",
        "icon_thumbnail",
    )

    def icon_thumbnail(self, obj):
        return mark_safe(
            '<img src="{url}" width={width} height={height} />'.format(
                url=obj.icon.url, width=50, height=50,
            )
        )

@admin.register(Counter)
class CounterAdmin(BaseAdmin):
    list_display = (
        "type",
        "count",
    )
