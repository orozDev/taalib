from django import template
from core.models import Categories

register = template.Library()

@register.simple_tag()
def categories():
    categories = Categories.objects.all()
    return categories