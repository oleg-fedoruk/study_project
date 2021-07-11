from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieShortSerializer, MovieFullSerializer


class MovieListView(APIView):
    """Вывод всех фильмов"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieShortSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод деталей фильма"""
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk)
        serializer = MovieFullSerializer(movie)
        return Response(serializer.data)
