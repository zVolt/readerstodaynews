# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User as BaseUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.utils.text import slugify
from indic_transliteration import sanscript


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    menu = models.IntegerField(default=0, choices=((0, "Main"), (1, "Secondary")))
    order = models.IntegerField(default=0)  # 0 no order
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("order",)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = CloudinaryField("image", blank=True)
    priority = models.IntegerField(default=0)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return "%r" % self.name


class Media(models.Model):
    title = models.CharField(max_length=50)
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=500, blank=True)
    image = CloudinaryField("image", blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=255)
    interested_categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.username


class Source(models.Model):
    name = models.CharField(max_length=100)
    followers = models.ManyToManyField(UserProfile, blank=True)
    icon = CloudinaryField("image", blank=True)

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=50)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=False, null=False)
    summary = models.TextField()
    content = models.TextField()
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(Category, blank=True)
    media_items = models.ManyToManyField(Media, blank=True)

    class Meta:
        ordering = ("last_modified_on",)

    def _create_slug(self):
        slug = slugify(self.title)
        if not slug:
            en_title = sanscript.transliterate(
                self.title, sanscript.DEVANAGARI, sanscript.HK
            )
            slug = slugify(en_title)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._create_slug()
        super(Post, self).save(*args, **kwargs)


class Counter(models.Model):
    type = models.CharField(max_length=100, unique=True)
    count = models.CharField(max_length=100, default="2347234")
