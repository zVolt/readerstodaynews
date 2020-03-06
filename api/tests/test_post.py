# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post, Category, PostType, Source
from django.contrib.auth.models import User
from .helper import login, create_user


def create_sample_posts():
    user = last_modified_by = User.objects.all().first()
    category1 = Category.objects.create(name="cat1", last_modified_by=user)
    category2 = Category.objects.create(name="cat2", last_modified_by=user)
    source = Source.objects.create(name="Source A")
    post_type = PostType.objects.create(name="news", last_modified_by=user)
    post1 = Post.objects.create(
        title="This is a title1",
        summary="summary",
        content="content",
        post_type=post_type,
        source=source,
        last_modified_by=user,
    )
    post1.categories.set([category1])

    post2 = Post.objects.create(
        title="This is a title2",
        summary="summary",
        content="content",
        post_type=post_type,
        source=source,
        last_modified_by=user,
    )
    post2.categories.set([category2])
    return [post1, post2]


class PostTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user()

    def test_fetch_detail_post_by_slug(self):
        create_sample_posts()
        url = reverse("api:post-detail", args=["this-is-a-title1"])
        response = self.client.get(url, format="json")
        self.assertEquals(response.data.get("title"), "This is a title1")

    def test_fetch_detail_post_by_id(self):
        pass

    def test_fetch_posts_by_category(self):
        create_sample_posts()
        response = self.client.get(
            reverse("api:post-list"), {"categories__name": "cat1"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data.get("results")), 1)

        response = self.client.get(
            reverse("api:post-list"), {"categories__name": "cat2"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data.get("results")), 1)

    def test_fetch_all_posts(self):
        create_sample_posts()
        response = self.client.get(reverse("api:post-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data.get("results")), 2)

    def test_create_post(self):
        login(self.client)
        data = {
            "title": "This is a Title",
            "summary": "This is a summary",
            "content": "This is post content",
            "post_type": "News",
            "source": "Twitter",
            "categories": ["Space" "Tech"],
        }

        url = reverse("api:post-list")
        response = self.client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
