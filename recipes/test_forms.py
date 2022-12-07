from django.test import TestCase

from .forms import CommentForm


class TestCommentForm(TestCase):
    def test_empty_fields(self):
        form = CommentForm(data={
            'content': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'][0], 'This field is required.')

    def test_valid_form(self):
        form = CommentForm(data={
            'content': 'Test content'
        })
        self.assertTrue(form.is_valid())
