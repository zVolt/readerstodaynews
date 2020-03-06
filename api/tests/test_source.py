# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Source
from .helper import login, create_user


class SourceTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user()

    def test_fetch_multiple_counter(self):
        Source.objects.create(name="a", icon="123")
        Source.objects.create(name="b", icon="123")
        url = reverse("api:source-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_create_source(self):
        login(self.client)
        url = reverse("api:source-list")
        data = {"name": "Facebook", "icon": "http://facebook.com/icon"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Source.objects.count(), 1)
