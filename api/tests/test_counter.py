# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Counter
from .helper import login, create_user


class CounterTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user()

    def test_fetch_multiple_counter(self):
        Counter.objects.create(type="a", count="123")
        Counter.objects.create(type="b", count="123")
        url = reverse("api:counter-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_create_counter(self):
        login(self.client)
        url = reverse("api:counter-list")
        data = {"type": "page_counter", "count": "8367"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Counter.objects.count(), 1)
