from django.urls import path, include
from main.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register('actors', ActorViewSet)
router.register('movies', MovieViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('subscriptions/', SubscriptionListCreateView.as_view()),

    path('token/', obtain_auth_token),
]
