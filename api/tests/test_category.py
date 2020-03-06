# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Category
from .helper import login, create_user
from django.contrib.auth.models import User


class CategoryTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user()

    def test_fetch_multiple_category(self):
        Category.objects.create(
            name="cat1", last_modified_by=User.objects.all().first()
        )
        Category.objects.create(
            name="cat2", last_modified_by=User.objects.all().first()
        )
        url = reverse("api:category-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_fetch_category(self):
        category = Category.objects.create(
            name="cat1", last_modified_by=User.objects.all().first()
        )
        url = reverse("api:category-detail", args=[category.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"name": "cat1", "id": 1, "image": ""})

    def test_create_multiple_categories(self):
        login(self.client)

        url = reverse("api:category-list")
        data = {"name": "category2"}  # [{"name": "category1"}, ]
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
