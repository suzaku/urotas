#-*- coding:utf-8 -*-

from django.db import models, IntegrityError
from django.contrib.auth.models import User

from urotas.local.models.fields import FormatDateTimeField

class Tag(models.Model):
    content = models.CharField(max_length=32, unique=True)
    creator = models.ForeignKey(User, related_name='tags_i_created')
    used = models.IntegerField(default=0) # 使用此标签的人数

    class Meta:
        ordering = ['-used']

class Note(models.Model):
    author = models.ForeignKey(User, related_name='notes')
    content = models.CharField(max_length=256)
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
        modified_f = self._meta.get_field_by_name('modified')[0]
        return {
                'id': self.id,
                'content': self.content,
                'modified': modified_f.value_to_string(self),
                'timestamp': self.modified.strftime('%Y-%m-%d %H:%M:%S.%f'),
                }

    @staticmethod
    def parse_for_tags(instance, **kwargs):
        tag_tokens = instance.content.split('#')
        if len(tag_tokens) >= 3:
            for token in tag_tokens[1:-1:2]:
                try:
                    tag = Tag(content=token, creator=instance.author)
                    tag.save()
                except IntegrityError:
                    tag = Tag.objects.get(content=token)
                
                try:
                    taggedNote = TaggedNote(note=instance, tag=tag)
                    taggedNote.save()
                except IntegrityError:
                    pass 

models.signals.post_save.connect(Note.parse_for_tags, sender=Note)

class TaggedNote(models.Model):
    note = models.ForeignKey(Note)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = (('note', 'tag'),)
