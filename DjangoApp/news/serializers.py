from .models import News, Comments
from rest_framework import serializers


class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)

    main_image = serializers.ImageField(allow_null=True, required=False)

    preview_image = serializers.ImageField(read_only=True)

    content = serializers.CharField()

    publication_date = serializers.DateTimeField(
        allow_null=True, required=False
    )

    author = serializers.CharField(required=False)

    def create(self, validated_data: dict) -> None:
        return News.objects.create(**validated_data)

    def update(self, instance: News, validated_data: dict) -> News:
        instance.title = validated_data.get('title', instance.title)
        instance.main_image = validated_data.get(
            'main_image', instance.main_image
        )
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)
    related_news = serializers.PrimaryKeyRelatedField(
        queryset=News.objects.all(), required=False
    )
    publication_date = serializers.DateTimeField(
        allow_null=True, required=False
    )

    def create(self, validated_data: dict) -> None:
        return Comments.objects.create(**validated_data)

    def update(self, instance: Comments, validated_data: dict) -> News:
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
