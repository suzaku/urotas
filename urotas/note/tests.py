"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

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
