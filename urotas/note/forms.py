from django import forms

class NoteForm(forms.Form):
    content = forms.CharField(max_length=128)

class QueryNotesByTimeForm(forms.Form):
    timestamp = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S.%f'],
                                    required=True)
    delta = forms.IntegerField(initial=10, min_value=1, required=False)

class SearchNoteForm(forms.Form):
    tag = forms.CharField(max_length=32)
