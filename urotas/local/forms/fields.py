#-*-coding=utf-8-*-

from django import forms

class CommaSeparatedField(forms.CharField):
    def clean(self, value):
        "Normalize data to a list of strings."
        value = super(CommaSeparatedField, self).clean(value)
        if not value:
            return []
        return value.split(',')
