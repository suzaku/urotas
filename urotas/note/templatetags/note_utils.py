#-*-coding=utf-8-*-

import time

from django import template
from django.utils.safestring import mark_safe

from note.utils import tag_linkify as _tag_linkify

register = template.Library()

@register.filter
def tag_linkify(value):
    return mark_safe(_tag_linkify(value))
