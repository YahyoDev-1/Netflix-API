from django.urls import path
from main.views import *

urlpatterns = [
    path('actors/', ActorView.as_view()),

    path('movies/', MovieView.as_view()),

    path('subscriptions/', SubscriptionListCreateView.as_view()),
]