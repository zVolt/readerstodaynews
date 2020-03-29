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
from rest_framework.response import Response
from rest_framework import authentication, viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated

from firebase_admin import auth

from reprlib import repr
import re
import json

from .models import Post, Category, UserProfile, MenuItem, Source, Counter, Media
from .serializers import (
    FullPostSerializer,
    BasicPostSerializer,
    CreatePostSerializer,
    CategorySerializer,
    SourceSerializer,
    MenuSerializer,
    CounterSerializer,
    MediaSerializer,
)
from .permissions import ReadOnly


class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    filterset_fields = [
        "menu",
    ]
    search_fields = ["name"]
    ordering_fields = ["order"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    lookup_field = "name"
    filterset_fields = [
        "name",
    ]
    search_fields = ["name"]
    ordering_fields = ["priority"]


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
    lookup_field = "slug"
    filterset_fields = ["categories__name", "source__name", "post_type__name", "slug"]
    search_fields = ["title", "content", "slug"]
    ordering_fields = ["last_modified_on"]

    def get_serializer_class(self):
        if self.action == "list":
            return BasicPostSerializer
        elif self.action in ["create", "update"]:
            return CreatePostSerializer
        else:
            return FullPostSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    filterset_fields = [
        "media_type",
    ]
    search_fields = ["media_type"]
    ordering_fields = ["title", "last_modified_on"]
