from urllib import response

from pyexpat.errors import messages
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


# Create your views here.

class ActorView(APIView):
    def get(self, request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActorRetrieveAPIView(APIView):
    def get(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActorUpdateAPIView(APIView):
    def put(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializer(actor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'message': 'Actor updated successfully',
            'new_actor': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class ActorDeleteAPIView(APIView):
    def delete(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        actor.delete()
        response = {
            'success': True,
            'message': 'Actor deleted successfully',
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class MovieView(APIView):
    def get(self, request):
        movies = Movie.objects.all().order_by('-id')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Movie, pk=pk)

    def get(self, request, pk):
        serializer = MovieSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = MovieSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'message': 'Movie updated successfully',
                'new_movie': serializer.data
            }
        )

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response({'success': True, 'message': 'Movie deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all().order_by('-id')
    serializer_class = SubscriptionSerializer


class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
