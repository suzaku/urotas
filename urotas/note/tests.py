#-*-coding=utf-8-*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Note, Tag
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester',
                                             'tester')
        self.note = Note(author=self.user, content='#test#')
        self.note.save()

    def test_author(self):
        self.assertEqual(self.note.author, self.user)
        self.assertEqual(self.user.notes.get(), self.note)

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

    def test_content_conversion(self):
        list_url = reverse('note.views.list')
        self.note.content = '#Tag:># message #Tag2#'
        self.note.save()
        self.assertEqual(self.note.content.html,
                        '<a href="'+list_url+
                        '?tags=Tag%3A%3E">#Tag:&gt;#</a> message <a href="'+
                        list_url+'?tags=Tag2">#Tag2#</a>')

class TagTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('tester1', 'tester1')
        self.tag = Tag(content="test", creator=self.user1)
        self.tag.save()

    def test_creator(self):
        self.assertEqual(self.tag.creator, self.user1)
        self.assertTrue(self.tag in self.user1.tags_i_created.all())
