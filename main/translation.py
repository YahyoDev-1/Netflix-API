from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Actor)
class ActorTranslation(TranslationOptions):
    fields = ('country', 'gender')

@register(Movie)
class MovieTranslation(TranslationOptions):
    fields = ('title', 'genre',)

@register(Subscription)
class SubscriptionTranslation(TranslationOptions):
    fields = ('title',)

@register(Review)
class ReviewTranslation(TranslationOptions):
    fields = ('comment',)