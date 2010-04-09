#-*-coding=utf-8-*-

from urllib import quote
import itertools

from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe

import re
TAG_PATTERN = re.compile(r'#[^#]+#')

class NoteContent(object):

    def __init__(self, content):
        self.text = content

        untagged_tokens = TAG_PATTERN.split(content)
        tagged_tokens = TAG_PATTERN.findall(content)
        self.tags = [tag[1:-1] for tag in tagged_tokens]

        if tagged_tokens:
            buf = []
            for untagged, tagged in itertools.izip_longest(untagged_tokens,
                                               tagged_tokens, fillvalue=''):
                if untagged:
                    buf.append(escape(untagged))
                if tagged:
                    buf.append('<a href="/note/search?tags=%s">%s</a>' % (
                                            quote(tagged[1:-1]), escape(tagged) ))
            self.html = mark_safe(''.join(buf))
        else:
            self.html = mark_safe(escape(content))

    def __unicode__(self):
        return self.html
