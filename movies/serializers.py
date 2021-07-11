from rest_framework import serializers

from .models import Movie


class MovieShortSerializer(serializers.ModelSerializer):
    """Сериализация трёх полей модели Movie"""
    class Meta:
        model = Movie
        fields = ('title', 'tagline')


class MovieFullSerializer(serializers.ModelSerializer):
    """Сериализация всех полей модели Movie"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
