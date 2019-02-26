from django import template

from ..utils import make_poster_url

register = template.Library()


@register.simple_tag
def poster_url(path, width):
    return make_poster_url(path, width)
