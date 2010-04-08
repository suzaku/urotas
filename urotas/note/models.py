#-*- coding:utf-8 -*-

from django.db import models, IntegrityError
from django.contrib.auth.models import User

from urotas.local.models.fields import (FormatDateTimeField,
                                        NoteContentField,)

class Tag(models.Model):
    """Tag

    Make sure that the `used` value of a tag is incremented everytime a note
    is tagged by it. Without this field, we have to count the records in the
    association table everytime we want to know how many time a certain tag
    has been used. Regularly, we need to sort tags by the times they are used
    and I think this is a way to improve performance.
    """
    content = models.CharField(max_length=32, unique=True)
    creator = models.ForeignKey(User, related_name='tags_i_created')
    used = models.IntegerField(default=0) # 使用此标签的人数

    users = models.ManyToManyField(User, through='TaggedNote',
                                  related_name='tags_i_used')

    class Meta:
        ordering = ['-used']

class Note(models.Model):
    """Note"""
    #TODO remove the `is_changable` field
    author = models.ForeignKey(User, related_name='notes')
    content = NoteContentField(max_length=256)
    created = FormatDateTimeField(format="n月j日 G:s",
                                  auto_now_add=True)
    modified = FormatDateTimeField(format="n月j日 G:s",
                                   auto_now=True)
    is_changable = models.BooleanField(default=True) # 是否可修改
    is_private = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through='TaggedNote', 
                                  related_name='notes')

    class Meta:
        ordering = ['-modified']

    def get_serializable(self):
        """Return a simple python dict that can be dumped by simplejson
        directly."""
        modified_f = self._meta.get_field_by_name('modified')[0]
        return {
                'id': self.id,
                'content': self.content.html,
                'modified': modified_f.value_to_string(self),
                'timestamp': self.modified.strftime('%Y-%m-%d %H:%M:%S.%f'),
                }

    @staticmethod
    def update_tags(instance, **kwargs):
        """Save `TaggedNote` objects according to tags contains in 
        `instance.cotent`. Create new tags if necessary."""
        # TODO 将不再包含的标签去掉, 增加新的标签
        for token in instance.content.tags:
            try:
                tag = Tag(content=token, creator=instance.author)
                tag.save()
            except IntegrityError:
                tag = Tag.objects.get(content=token)
            
            try:
                taggedNote = TaggedNote(note=instance, tag=tag,
                                        tagged_by=instance.author)
                taggedNote.save()
            except IntegrityError:
                pass 
models.signals.post_save.connect(Note.update_tags, sender=Note,
                                 dispatch_uid="note.models.note")

class TaggedNote(models.Model):
    """Assocation Table of Tag and Note
    `tagged_by` field is designed for the performance and convinience of 
    retrieving all tags used by a user.
    """
    note = models.ForeignKey(Note)
    tag = models.ForeignKey(Tag)
    tagged_by = models.ForeignKey(User)

    class Meta:
        unique_together = (('note', 'tag'),)

    @staticmethod
    def inc_tag_used(instance, **kwargs):
        """Increment the `used` field"""
        tag = instance.tag
        tag.used += 1
        tag.save()

    @staticmethod
    def dec_tag_used(instance, **kwargs):
        """Decrement the `used` field"""
        tag = instance.tag
        tag.used -= 1
        tag.save()
models.signals.post_save.connect(TaggedNote.inc_tag_used, sender=TaggedNote,
                                 dispatch_uid="note.models.tagged_note")
models.signals.pre_delete.connect(TaggedNote.dec_tag_used, sender=TaggedNote,
                                  dispatch_uid="note.models.tagged_note")
