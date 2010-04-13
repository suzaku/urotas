#-*-coding=utf-8-*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Note, Tag
from django.contrib.auth.models import User

class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester',
                                             'tester')
        self.note = Note(author=self.user, content='#test#')
        self.note.save()

    def test_get_serializable(self):
        note_dict = self.note.get_serializable()
        self.assertEqual(note_dict['id'], self.note.id)
        self.assertEqual(note_dict['content'], self.note.content.html)
        from django.utils.dateformat import format
        self.assertEqual(note_dict['modified'], 
                         format(self.note.modified, 'n月j日 G:s'))
        self.assertEqual(note_dict['timestamp'],
                         self.note.modified.strftime('%Y-%m-%d %H:%M:%S.%f'))

    def test_update_tags(self):
        orig_tags = self.note.tags.all()
        self.assertTrue(Tag.objects.get(content='test') in orig_tags)
        self.note.content = '#new test# ok #a third one#'
        self.note.save()
        new_tags = self.note.tags.all()
        self.assertFalse(Tag.objects.get(content='test') in new_tags)
        self.assertTrue(Tag.objects.get(content='new test') in new_tags)
        self.assertTrue(Tag.objects.get(content='a third one') in new_tags)


"""
from utils import tag_linkify
class NoteTest(TestCase):
    def setUp(self):
        self.content_without_tag = 'nothing about tag'
        self.content = '#Tag:># message #Tag2#'
        self.linkified_content = '<a href="/note/search?tag=Tag%3A%3E">#Tag:&gt;#</a> message <a href="/note/search?tag=Tag2">#Tag2#</a>'

    def test_note_tag_to_link(self):
        self.assertEqual(self.content_without_tag,
                         tag_linkify(self.content_without_tag))
        self.assertEqual(self.linkified_content,
                         tag_linkify(self.content))
"""
