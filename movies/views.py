from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Actor
from .serializers import \
    (MovieShortSerializer,
     MovieFullSerializer,
     ReviewFullSerializer,
     CreateRatingSerializer,
     ActorShortSerializer,
     ActorFullSerializer)
from .service import get_client_ip


class MovieListView(APIView):
    """Вывод всех фильмов"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = MovieShortSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод деталей фильма"""
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk)
        serializer = MovieFullSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Создание отзыва"""
    def post(self, request):
        review = ReviewFullSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга к фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    """Вывод списка актёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorShortSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод детальной информации об актёре или режиссере"""
    queryset = Actor.objects.all()
    serializer_class = ActorFullSerializer
