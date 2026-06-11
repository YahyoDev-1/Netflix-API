from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Language)
class Language(TranslationOptions):
    fields = ('name',)