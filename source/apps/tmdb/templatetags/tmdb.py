from django import template

register = template.Library()


@register.simple_tag
def poster_url(path, width):
    widths = ["original", "w92", "w154", "w185", "w342", "w500", "w780"]
    return f"https://image.tmdb.org/t/p/{widths[width]}{path}"
