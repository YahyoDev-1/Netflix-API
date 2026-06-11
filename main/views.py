from django.utils import translation
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status, response
from rest_framework.response import Response
from rest_framework import filters
from .serializers import *
from .models import *
import django_filters

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
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_date',)
    filterset_fields = ('country', 'gender',)

    def get_queryset(self):

        lang = self.request.query_params.get('lang', ) or self.request.headers.get('Accept-Language', 'uz')

        translation.activate(lang)

        return super().get_queryset()


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


class ReviewViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.action in ["reviews"]:
            return MovieSerializer
        return ReviewSerializer

    # Filmga tegishli sharhlarni ko'rish (GET) va yangi sharh yozish (POST)
    @action(detail=True, methods=['get', 'post'], url_path='reviews')
    def reviews(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        # GET so'rovi bo'lganda sharhlar ro'yxatini qaytaramiz
        if request.method == 'GET':
            reviews = movie.reviews.all()  # related_name='reviews'
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        # POST so'rovi bo'lganda yangi sharh yaratamiz
        elif request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Sharhni saqlaymiz va unga ushbu filmni hamda so'rov yuborgan foydalanuvchini biriktiramiz
            serializer.save(movie=movie, user=request.user)

            # Yangi yaratilgan sharh ma'lumotlarini 201 status bilan qaytaramiz
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # O'chirilmoqchi bo'lgan izoh egasi hozirgi foydalanuvchi bilan bir xilligini tekshiramiz
        if instance.user != self.request.user:
            raise PermissionDenied(
                {"detail": "Siz faqat o'zingiz yozgan sharhlarni o'chira olasiz!"}
            )

        # Agar foydalanuvchiniki bo'lsa, o'chirib yuboramiz
        instance.delete()

    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('user.username',)
    ordering_fields = ('rate', 'created_at',)
    filterset_fields = ('user.username', 'movie.title')


class RateFilter(django_filters.FilterSet):
    min_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='gte')
    max_rate = django_filters.NumberFilter(field_name='rate', lookup_expr='lte')

    class Meta:
        model = Review
        fields = ['min_rate', 'max_rate']