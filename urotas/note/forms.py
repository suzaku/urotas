#-*-coding=utf-8-*-
from django import forms
from models import Note

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

class QueryNotesByTimeForm(forms.Form):
    """查询微记"""
    timestamp = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S.%f'],
                                    required=True)
    delta = forms.IntegerField(initial=10, min_value=1, required=False)

    def fetch_notes(self, queryset):
        timestamp = self.cleaned_data['timestamp']
        delta = self.cleaned_data['delta']
        notes = queryset.filter(modified__lt=timestamp).all()[:delta]
        return notes

# TODO 是否合并到QueryNotesByTimeForm?
class SearchNoteForm(forms.Form):
    """根据标签查询微记"""
    tag = forms.CharField(max_length=32)
