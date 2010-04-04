#-*-coding=utf-8-*-

from urllib import quote
import itertools

from django.conf import settings
from django.utils.html import escape

import re
TAG_PATTERN = re.compile(r'#[^#]+#')

def linkify(content):
    untagged_tokens = TAG_PATTERN.split(content)
    tagged_tokens = TAG_PATTERN.findall(content)
    if tagged_tokens:
        buf = []
        for untagged, tagged in itertools.izip_longest(untagged_tokens,
                                           tagged_tokens, fillvalue=''):
            if untagged:
                buf.append(escape(untagged))
            if tagged:
                buf.append('<a href="/note/search?tag=%s">%s</a>' % (
                                        quote(tagged[1:-1]), escape(tagged) ))
        return ''.join(buf)
    else:
        return escape(content)
