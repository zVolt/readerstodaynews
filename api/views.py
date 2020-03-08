# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated

from firebase_admin import auth

from reprlib import repr
import re
import json

from .models import Post, Category, UserProfile, MenuItem, Source, Counter
from .serializers import (
    FullPostSerializer,
    BasicPostSerializer,
    CreatePostSerializer,
    CategorySerializer,
    SourceSerializer,
    MenuSerializer,
    CounterSerializer,
)
from .permissions import ReadOnly


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        id_token = request.data.get("token")
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        auth_user = auth.get_user(uid)
        name, email, photo_url = (
            auth_user.display_name,
            auth_user.email,
            auth_user.photo_url,
        )
        user = User.objects.filter(email=email).first()
        user_profile = UserProfile.objects.filter(user=user).first() if user else None
        res = {}
        if not user_profile:
            username = email.split("@")[0]
            user = User.objects.create(
                username=username, first_name=name, email=email, password=""
            )
            user.save()
            user_profile = UserProfile(user=user, profile_pic=photo_url)
            user_profile.save()
        if user and user_profile:
            token, created = Token.objects.get_or_create(user=user_profile.user)
            res["user_id"] = user_profile.pk
            res["email"] = user_profile.user.email
            res["username"] = user_profile.user.username
            res["name"] = user_profile.user.get_full_name()
            res["photo_url"] = user_profile.profile_pic
            res["token"] = token.key
        return Response(res)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    filterset_fields = [
        "menu",
    ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    lookup_field = "name"
    filterset_fields = [
        "name",
    ]


class CounterViewSet(viewsets.ModelViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    lookup_field = "type"


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated | ReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated | ReadOnly]
    filterset_fields = ["categories__name", "source__name", "post_type__name"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return BasicPostSerializer
        elif self.action in ["create", "update"]:
            return CreatePostSerializer
        else:
            return FullPostSerializer
