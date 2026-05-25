from rest_framework import serializers
from .models import *


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

# class ActorForMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Actor
#         fields = ('id', 'name')


class MovieSerializer(serializers.ModelSerializer):
    # actors = ActorForMovieSerializer(many=True, read_only=True)

    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Movie
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(min_value=0, max_value=5)
    movie = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Review
        fields = ['id', 'movie', 'comment', 'rate', 'user', 'created_at']