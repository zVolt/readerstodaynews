from django.contrib.auth.models import User


def login(client):
    client.login(username="test", password="test")


def create_user():
    User.objects.create_user("test", password="test")
