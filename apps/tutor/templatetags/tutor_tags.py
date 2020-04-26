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

@register.filter(name='uppercase')
def to_upper_case(text):
    txt = text.split(' ')
    for i, string in enumerate(txt):
        string = string[0].upper() + string[1:]
        txt[i] = string
    return mark_safe(
        ' '.join(txt)
    )