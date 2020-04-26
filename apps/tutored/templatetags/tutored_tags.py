# Django
from django import template
from django.utils.safestring import mark_safe

# Constants
from doceo.constants import SUBAREAS

register = template.Library()

@register.filter(name='uppercase')
def to_upper_case(text):
    txt = text.split(' ')
    for i, string in enumerate(txt):
        string = string[0].upper() + string[1:]
        txt[i] = string
    return mark_safe(
        ' '.join(txt)
    )

@register.filter(name='verbose_name')
def get_verbose_name(text):
    only_subareas_array = [subarea[1] for subarea in SUBAREAS]
    subarea = [subarea[1] for subareas in only_subareas_array for subarea in subareas if subarea[0] == text]
    return subarea[0]