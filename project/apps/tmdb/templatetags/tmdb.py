from django import template

register = template.Library()


@register.simple_tag
def poster_url(path, width):
    widths = ["original", "w92", "w154", "w185", "w342", "w500", "w780"]
    return "https://image.tmdb.org/t/p/{}{}".format(widths[width], path)
