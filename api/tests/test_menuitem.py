# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import MenuItem, Category
from django.contrib.auth.models import User
from .helper import login, create_user


class MenuItemTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user()

    def test_get_menu(self):
        MenuItem.objects.create(
            name="Login", url="/login", last_modified_by=User.objects.all().first()
        )
        MenuItem.objects.create(
            name="Logout", url="/logout", last_modified_by=User.objects.all().first()
        )
        response = self.client.get(reverse("api:menu-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_create_menu_item(self):
        login(self.client)
        url = reverse("api:menu-list")
        data = {"name": "Sign up", "id": 1, "url": "/signup", "menu": 1, "order": 0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 1)
