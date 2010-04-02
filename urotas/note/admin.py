#-*- coding:utf-8 -*-
from django.contrib import admin
from models import Tag, Note, TaggedNote

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class NoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Note, NoteAdmin)

class TaggedNoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(TaggedNote, TaggedNoteAdmin)
