#-*-coding=utf-8-*-
from django.utils import datetime_safe
from django.utils.dateformat import format
from django.db import models

from ..utils import NoteContent

class FormatDateTimeField(models.DateTimeField):
    """A datetime field that support a `format` parameter.

    When the `value_to_string` method is called, the datetime
    object will be transformed to the specified format.
    """
    def __init__(self, **kwargs):
        try:
            self.format = kwargs.pop('format')
        except KeyError:
            self.format = '%Y-%m-%d %H:%M:%S'
        super(FormatDateTimeField, self).__init__(**kwargs)

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            d = datetime_safe.new_datetime(val)
            data = format(d, self.format)
        return data

class NoteContentField(models.CharField):
    """笔记内容
    自动将内容中的标签记号封装成对应的查询链接.
    """

    # For detail: http://docs.djangoproject.com/en/dev/howto/custom-model-fields/#the-subfieldbase-metaclass
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        # DONE 返回一个带有text, html, tags等属性的对象
        value = super(NoteContentField, self).to_python(value)
        return NoteContent(value)

    def get_db_prep_value(self, value):
        return value.text
