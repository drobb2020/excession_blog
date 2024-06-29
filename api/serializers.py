from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from a_services.models import Review

from a_blog.models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = (
            "slug",
            "title",
            "subtitle",
            "author",
            "content",
            "post_image",
            "published_date",
            "status",
            "tags",
            "is_featured",
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "user",
            "email",
            "review_title",
            "comment",
            "created_at",
            "approved",
        )
