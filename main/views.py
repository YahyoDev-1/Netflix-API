from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from rest_framework import permissions, status, response
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


# Create your views here.

# class ActorView(APIView):
#     def get(self, request):
#         actors = Actor.objects.all()
#         serializer = ActorSerializer(actors, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ActorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ActorRetrieveAPIView(APIView):
#     def get(self, request, pk):
#         actor = get_object_or_404(Actor, pk=pk)
#         serializer = ActorSerializer(actor)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class ActorUpdateAPIView(APIView):
#     def put(self, request, pk):
#         actor = get_object_or_404(Actor, pk=pk)
#         serializer = ActorSerializer(actor, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = {
#             'success': True,
#             'message': 'Actor updated successfully',
#             'new_actor': serializer.data
#         }
#         return Response(response, status=status.HTTP_200_OK)
#
#
# class ActorDeleteAPIView(APIView):
#     def delete(self, request, pk):
#         actor = get_object_or_404(Actor, pk=pk)
#         actor.delete()
#         response = {
#             'success': True,
#             'message': 'Actor deleted successfully',
#         }
#         return Response(response, status=status.HTTP_204_NO_CONTENT)

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


# class MovieView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all().order_by('-id')
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class MovieRetrieveUpdateDestroyAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Movie, pk=pk)
#
#     def get(self, request, pk):
#         serializer = MovieSerializer(self.get_object(pk))
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         serializer = MovieSerializer(self.get_object(pk), data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Movie updated successfully',
#                 'new_movie': serializer.data
#             }
#         )
#
#     def delete(self, request, pk):
#         movie = self.get_object(pk)
#         movie.delete()
#         return Response({'success': True, 'message': 'Movie deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_class(self):
        # DIQQAT: "add-actor" emas, metod nomi "add_actor" bo'lishi shart!
        if self.action in ["actors", "add_actor"]:
            return ActorSerializer
        return MovieSerializer

    @action(detail=True, methods=['get'])
    def actors(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        actors = movie.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-actor')
    def add_actor(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        # Kelayotgan ma'lumotlarni ActorSerializer orqali validatsiya qilamiz
        serializer = ActorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Yangi aktyorni bazaga saqlaymiz
        actor = serializer.save()

        # Many-to-Many aloqasi orqali aktyorni filmga biriktiramiz
        movie.actors.add(actor)

        # Javob qaytaramiz
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubscriptionListCreateView(ListCreateAPIView):
    queryset = Subscription.objects.all().order_by('-id')
    serializer_class = SubscriptionSerializer


class SubscriptionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
