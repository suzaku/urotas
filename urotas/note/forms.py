from django import forms

class NoteForm(forms.Form):
    content = forms.CharField(max_length=128)
