"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Note
from django.contrib.auth.models import User

class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester',
                                             'tester')
        self.note = Note(author=self.user, content='#test#')
        self.note.save()

    def test_get_serializable(self):
        note_dict = self.note.get_serializable()
        self.assertEqual(note_dict['content'], 
                         self.note.content.html)

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
