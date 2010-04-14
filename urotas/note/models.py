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
    users = models.ManyToManyField(User, through='TaggedNote',
                                  related_name='tags_i_used')

    def __eq__(self, other):
        return super(Tag, self).__eq__(other) and (self.content == other.content)

    def __unicode__(self):
        return '<Tag: %s>' % self.content

class Note(models.Model):
    """Note"""
    author = models.ForeignKey(User, related_name='notes')
    content = NoteContentField(max_length=256)
    created = FormatDateTimeField(format="n月j日 G:s",
                                  auto_now_add=True)
    modified = FormatDateTimeField(format="n月j日 G:s",
                                   auto_now=True)
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
        old_tags = list(instance.tags.all())
        for token in instance.content.tags:
            tag, t_is_new = Tag.objects.get_or_create(content=token,
                                defaults={'creator':instance.author})

            taggedNote, tn_is_new = TaggedNote.objects.get_or_create(
                                    note=instance, tag=tag,
                                    defaults={'tagged_by':instance.author})
            if tag in old_tags:
                # old tags that remain in the content are removed from
                # the `old_tags` list, which in the end contains only 
                # tags that are not longer used by `instance`
                old_tags.remove(tag)

        for tag in old_tags:
            taggedNote = TaggedNote.objects.get(note=instance,
                                                tag=tag)
            taggedNote.delete()
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
