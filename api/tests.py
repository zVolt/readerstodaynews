# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import MenuItem


class MenuItemTests(APITestCase):
    def test_create_menu_item(self):
        url = reverse("menu-list")
        data = [
            {"name": "Sign up", "id": 1, "url": "/signup", "menu": 1, "order": 0},
            {"name": "Log in", "id": 2, "url": "/login", "menu": 1, "order": 0},
        ]
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)
