from django.db import models


class Counter(models.Model):
    counter = models.CharField(max_length=100, default="2347234")
