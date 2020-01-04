# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User as BaseUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings



class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    menu = models.IntegerField(default=0, choices=((0, 'Main'), (1, 'Secondary'))) # 0 primary, 1 secondary
    order = models.IntegerField(default=0) # 0 no order
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image', blank=True)
    priority = models.IntegerField(default=0)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%r' % self.name


class Media(models.Model):
    title = models.CharField(max_length=50)
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=500, blank=True)
    image = CloudinaryField('image', blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=255)
    interested_tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    last_modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s' % (self.user.user.username, self.content)


class Source(models.Model):
    name = models.CharField(max_length=100)
    followers = models.ManyToManyField(UserProfile, blank=True)
    icon = CloudinaryField('image', blank=True)

    def __str__(self):
        return self.name

class PostType(models.Model):
    name = models.CharField(max_length=50)
    last_modified_on = models.DateTimeField()
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField()
    content = models.TextField()
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    last_modified_on = models.DateTimeField()
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    media_items = models.ManyToManyField(Media, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    likes = models.ManyToManyField(UserProfile, blank=True)
    share_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('last_modified_on',)
