from django.utils import datetime_safe
from django.utils.dateformat import format
from django.db import models

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
