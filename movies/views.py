from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Movie, Actor
from .serializers import \
    (MovieShortSerializer,
     MovieFullSerializer,
     ReviewFullSerializer,
     CreateRatingSerializer,
     ActorShortSerializer,
     ActorFullSerializer)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод всех фильмов"""
    serializer_class = MovieShortSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод деталей фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieFullSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Создание отзыва"""
    serializer_class = ReviewFullSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    """Вывод списка актёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorShortSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод детальной информации об актёре или режиссере"""
    queryset = Actor.objects.all()
    serializer_class = ActorFullSerializer
