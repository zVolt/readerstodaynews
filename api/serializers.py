import cloudinary
from django.db import transaction
from rest_framework import serializers
from .models import (
    Counter,
    UserProfile,
    MenuItem,
    Category,
    MediaType,
    Source,
    Media,
    PostType,
    Post,
    BaseUser,
)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = ("username", "profile_pic", "id")
        validators = []


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("name", "id", "url", "menu", "order")

    def create(self, validated_data):
        request = self.context.get("request")
        return MenuItem.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "id", "image")

    def to_representation(self, instance):
        representation = super(CategorySerializer, self).to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.build_url(secure=True)
        return representation

    def create(self, validated_data):
        request = self.context.get("request")
        return Category.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ("name", "id")

    def create(self, validated_data):
        request = self.context.get("request")
        return Media.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class SourceSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField(read_only=True)

    def get_follower_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = Source
        fields = ("name", "icon", "follower_count", "id")

    def to_representation(self, instance):
        representation = super(SourceSerializer, self).to_representation(instance)
        if instance.icon:
            representation["icon"] = instance.icon.url
        return representation


class MediaSerializer(serializers.ModelSerializer):
    media_type = MediaTypeSerializer()

    class Meta:
        model = Media
        fields = ("media_type", "image", "video_url", "title", "id")
        validators = []

    def to_representation(self, instance):
        representation = super(MediaSerializer, self).to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.build_url(secure=True)
        return representation

    def create(self, validated_data):
        request = self.context.get("request")
        return Media.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ("name", "id")

    def create(self, validated_data):
        request = self.context.get("request")
        return PostType.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class BasicPostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    media_items = MediaSerializer(many=True, required=False)
    source = SourceSerializer(read_only=True)
    post_type = PostTypeSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "slug",
            "title",
            "summary",
            "source",
            "categories",
            "media_items",
            "last_modified_on",
            "post_type",
        )
        validators = []


class FullPostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    media_items = MediaSerializer(many=True, required=False)
    source = SourceSerializer()
    post_type = PostTypeSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "slug",
            "title",
            "summary",
            "source",
            "content",
            "categories",
            "media_items",
            "last_modified_on",
            "post_type",
        )


class CreatePostSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False
    )
    media_items = MediaSerializer(many=True, required=False)
    source = serializers.CharField(max_length=10)
    post_type = serializers.CharField(max_length=10)

    class Meta:
        model = Post
        fields = (
            "title",
            "summary",
            "source",
            "content",
            "categories",
            "media_items",
            "post_type",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        defaults = {"last_modified_by": request.user}
        source, _ = Source.objects.get_or_create(name=validated_data.pop("source"))
        categories = [
            Category.objects.get_or_create(name=cat, defaults=defaults)[0]
            for cat in validated_data.pop("categories", [])
        ]
        post_type, _ = PostType.objects.get_or_create(
            name=validated_data.pop("post_type"), defaults=defaults
        )

        media_items = []
        for media in validated_data.pop("media_items", []):
            media_type, _ = MediaType.objects.get_or_create(
                defaults=defaults, **media.pop("media_type")
            )
            media_items.append(
                MenuItem.objects.get_or_create(
                    media_type=media_type, defaults=defaults, **media,
                )[0]
            )
        post = Post.objects.create(
            last_modified_by=request.user,
            source=source,
            post_type=post_type,
            **validated_data,
        )
        post.categories.set(categories)
        post.media_items.set(media_items)
        return post

    def to_representation(self, instance):
        return FullPostSerializer().to_representation(instance)


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = (
            "id",
            "type",
            "count",
        )
