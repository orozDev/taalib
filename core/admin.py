from django.contrib import admin
from .models import Categories, Articles, Videos
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _


class ArticlesAdminForm(forms.ModelForm):
    content_ky = forms.CharField(label='Контент[ky]', widget=CKEditorUploadingWidget())
    content_ru = forms.CharField(label='Контент[ru]', widget=CKEditorUploadingWidget())

    class Meta:
        model = Articles
        fields = '__all__'


@admin.register(Articles)
class ArticlesAdmin(TranslationAdmin):
    list_display = ('title', 'created_at', 'author', 'is_published', 'views',)
    list_filter = ['created_at', 'author', 'is_published',]
    search_fields = ('title__icontains',)
    readonly_fields = ('views', 'created_at', 'get_image', 'updated_at',)
    fields = (
        'title_ru',
        'title_ky',
        'image',
        'get_image',
        'short_content_ru',
        'short_content_ky',
        'content_ru',
        'content_ky',
        'categories',
        'author',
        'is_published',
        'views',
        'created_at',
        'updated_at',
    )
    form = ArticlesAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="" width="50%">')

    get_image.short_description = _('Изображение')


@admin.register(Videos)
class Videosdmin(TranslationAdmin):
    list_display = ('title', 'created_at', 'author', 'is_published',)
    list_filter = ['created_at', 'author', 'updated_at']
    search_fields = ('title__icontains',)
    readonly_fields = ('created_at', 'updated_at',)
    fields = (
        'title_ru',
        'title_ky',
        'short_content_ru',
        'short_content_ky',
        'url',
        'categories',
        'author',
        'is_published',
        'created_at',
        'updated_at',
    )


@admin.register(Categories)
class CategoriesAdmin(TranslationAdmin):
    list_display = ('title', 'created_at',)
    readonly_fields = ('created_at', 'updated_at',)

# Register your models here.
