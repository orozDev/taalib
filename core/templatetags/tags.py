from django import template
from core.models import Categories, Videos
from core.views import LIST_CITIES
import datetime, locale, sys, json


if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

ISLAMIC_MONTH = [
    'мухаррам',
    'сафар',
    'раби аль-авваль',
    'раби ас-сани',
    'джумада аль-уля',
    'джумада ас-сани ',
    'раджаб',
    'шабан',
    'рамадан',
    'шавваль',
    'зу-ль-када',
    'зу-ль-хиджа',
]


register = template.Library()

@register.simple_tag()
def categories():
    categories = Categories.objects.all()
    return categories


@register.simple_tag()
def get_cities():
    return LIST_CITIES


@register.simple_tag()
def get_last_video():
    return Videos.objects.first()


@register.filter(name='apiDate')
def apiDate(val):
    result = datetime.datetime.strptime(val, '%Y-%m-%d').strftime('%-d %B %-Y года')
    return result


@register.filter(name='apiIslamicDate')
def apiIslamicDate(val):
    month = ISLAMIC_MONTH[int(val[4:6])-1]
    result = datetime.datetime.strptime(val, '%Y-%m-%d').strftime(f'%-d {month} %-Y')
    return result


@register.filter(name='json')
def convertJson(val):
    temp = str(val)
    print(temp)
    return json.dumps(val)