from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from .models import Movie, Actor
from .serializers import \
    (MovieShortSerializer,
     MovieFullSerializer,
     ReviewFullSerializer,
     CreateRatingSerializer,
     ActorShortSerializer,
     ActorFullSerializer)
from .service import get_client_ip, MovieFilter, MoviePagination


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод всех фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = MoviePagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            movies = Movie.objects.filter(draft=False).annotate(
                rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
        elif self.action == 'retrieve':
            movies = Movie.objects.filter(draft=False)
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieShortSerializer
        elif self.action == 'retrieve':
            return MovieFullSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Создание отзыва к фильму"""
    serializer_class = ReviewFullSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка актёров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorShortSerializer
        elif self.action == 'retrieve':
            return ActorFullSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод детальной информации об актёре или режиссере"""
    queryset = Actor.objects.all()
    serializer_class = ActorFullSerializer
