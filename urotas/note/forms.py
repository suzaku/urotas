#-*-coding=utf-8-*-
from django import forms
from models import Note

from local.forms import CommaSeparatedField

class ModifyNoteForm(forms.Form):
    """修改微记"""
    id = forms.IntegerField()
    content = forms.CharField(max_length=128)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ModifyNoteForm, self).__init__(*args, **kwargs)

    def clean_id(self):
        id = self.cleaned_data["id"]
        try:
            self.note = Note.objects.get(id=id)
            if self.user == self.note.author:
                return id
            else:
                raise forms.ValidationError("只有微博的作者可以修改该内容")
        except Note.DoesNotExist:
            raise forms.ValidationError("找不到这个微记")

    def save(self, commit=True):
        """保存Note.content字段"""
        self.note.content = self.cleaned_data['content']
        if commit:
            self.note.save()
        return self.note

class NewNoteForm(forms.Form):
    """创建新微记"""
    content = forms.CharField(max_length=128)

class QueryNoteForm(forms.Form):
    # TODO Make a reusable query form based on this class
    tags = CommaSeparatedField(max_length=128, required=False)
    timestamp = forms.DateTimeField(input_formats=('%Y-%m-%d %H:%M:%S.%f',),
                                    required=False)
    # TODO what's a proper value for initial `delta`
    delta = forms.IntegerField(initial=10, min_value=1, required=False)

    def clean_delta(self):
        # TODO is there a better way to set default of a field
        delta = self.cleaned_data['delta']
        if delta is None:
            return self.fields['delta'].initial
        else:
            return delta

    def filter_tags(self, queryset):
        tag_names = self.cleaned_data['tags']
        return queryset.filter(tags__content__in=tag_names)

    def filter_timestamp(self, queryset):
        timestamp = self.cleaned_data['timestamp']
        return queryset.filter(modified__lt=timestamp)

    def get_filtered_queryset(self, queryset):
        """For every field you can define a filter method named 
        filter_`field name`. `get_filtered_queryset` when called 
        will invoke these methods if the corresponding field has a
        non-None value.
        """
        for k, v in self.cleaned_data.items():
            if v:
                filter_name = ('filter_%s' % k)
                try:
                    queryset = getattr(self, filter_name)(queryset)
                except AttributeError:
                    continue
        return queryset

    # TODO what about a better self-describing name?
    def before_return(self, queryset):
        delta = self.cleaned_data['delta']
        return queryset.all()[:delta]

    def fetch_records(self, queryset):
        """It calls `get_filtered_queryset` for the ready-for-return 
        queryset, and send the result to `before_return`, in which
        the queryset is turn into a record set."""
        queryset = self.get_filtered_queryset(queryset)
        return self.before_return(queryset)
