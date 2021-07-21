from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieShortSerializer(serializers.ModelSerializer):
    """Сериализация 4 полей модели Movie"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'middle_star')


class ActorShortSerializer(serializers.ModelSerializer):
    """Сериализация 3 полей модели Actor"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorFullSerializer(serializers.ModelSerializer):
    """Сериализация всех полей модели Actor"""

    class Meta:
        model = Actor
        fields = '__all__'


class ReviewFullSerializer(serializers.ModelSerializer):
    """Сериализация отзывов"""

    class Meta:
        model = Review
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    """Рекусрсивный вывод children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewDeatailSerializer(serializers.ModelSerializer):
    """Сериализация отзывов"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга фильму пользователем"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


class MovieFullSerializer(serializers.ModelSerializer):
    """Сериализация всех полей модели Movie"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorShortSerializer( read_only=True, many=True)
    actors = ActorShortSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewDeatailSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
