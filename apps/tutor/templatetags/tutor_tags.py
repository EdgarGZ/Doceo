# Django
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='addunderscore')
def add_underscore(text):
    txt = text.split(' ')
    return mark_safe(
        '_'.join(txt)
    )