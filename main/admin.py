from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *


# Register your models here.


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ('country', 'gender')


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'genre')


@admin.register(Subscription)
class SubscriptionAdmin(TranslationAdmin):
    list_display = ('title',)


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = ('comment',)
