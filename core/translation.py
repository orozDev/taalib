from modeltranslation.translator import register, TranslationOptions
from .models import Categories, Articles, Videos


@register(Categories)
class CategoriesTranslationOption(TranslationOptions):
    fields = (
        'title',
    )


@register(Articles)
class ArticlesTranslationOption(TranslationOptions):
    fields = (
        'title',
        'short_content',
        'content',
    )


@register(Videos)
class VideosTranslationOption(TranslationOptions):
    fields = (
        'title',
        'short_content',
    )