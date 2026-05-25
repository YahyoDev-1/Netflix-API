from django.urls import path, include
from main.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('actors', ActorViewSet)
router.register('movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('subscriptions/', SubscriptionListCreateView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),
]
