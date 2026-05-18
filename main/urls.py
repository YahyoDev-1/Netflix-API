from django.urls import path
from main.views import *

urlpatterns = [
    path('actors/', ActorView.as_view()),

    path('actors/<int:pk>/details/', ActorRetrieveAPIView.as_view()),

    path('actors/<int:pk>/update/', ActorUpdateAPIView.as_view()),

    path('actors/<int:pk>/delete/', ActorDeleteAPIView.as_view()),

    path('movies/', MovieView.as_view()),

    path('movies/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view()),

    path('subscriptions/', SubscriptionListCreateView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),
]