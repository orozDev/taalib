from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from PIL import Image

LIIMIT_SIZE = 1200


class TimeStampMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата добавление'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата изменения'))

    class Meta:
        abstract = True


class Categories(TimeStampMixin):
    
    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        ordering = ['-created_at']

    title = models.CharField(max_length=150, verbose_name=_('название'))

    def __str__(self):
        return self.title


class Articles(TimeStampMixin):
    class Meta:
        verbose_name = _('статья')
        verbose_name_plural = _('статьи')
        ordering = ['-created_at']

    image = models.ImageField(upload_to='news_image/', verbose_name=_('изображение'))
    title = models.CharField(max_length=250, verbose_name=_('заголовок'))
    short_content = models.CharField(max_length=900, verbose_name=_('краткое описание'))
    content = models.TextField(verbose_name=_('контент'))
    categories = models.ManyToManyField('Categories', verbose_name=_('категории'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('автор'))
    views = models.IntegerField(default=0, null=True, verbose_name=_('просмотры'))
    is_published = models.BooleanField(default=True, verbose_name=_('опубликовать'))


    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        img.save(self.image.path, quality=20, optimize=True)

    def __str__(self):
        return f'{self.title}'


class Videos(TimeStampMixin):
    class Meta:
        verbose_name = _('видео ролик')
        verbose_name_plural = _('видео ролики')
        ordering = ['-created_at']

    title = models.CharField(max_length=250, verbose_name=_('заголовок'))
    short_content = models.CharField(max_length=400, verbose_name=_('краткое описание'))
    categories = models.ManyToManyField('Categories', verbose_name=_('категории'))
    url = models.URLField(verbose_name=_('ссылка на видео'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('автор'))
    is_published = models.BooleanField(default=True, verbose_name=_('опубликовать'))

    def __str__(self):
        return f'{self.title}'

# Create your models here.
