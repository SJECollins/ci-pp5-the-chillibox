import datetime
import pytz
from django.test import TestCase
from unittest import mock
from django.contrib.auth.models import User


from .models import Recipe, Comment, SubmittedRecipe


class TestRecipe(TestCase):
    """
    Test recipe model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.save()

    def test_recipe(self):
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            recipe = Recipe.objects.create(
                user=self.user,
                title='Test title',
                intro='Test intro',
                ingredients='Test ingredients',
                directions='Test directions',
                outro='Test outro',
                excerpt='Test excerpt',
                created=mocked,
                updated=mocked,
            )
        recipe_string = 'Test title'
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(str(recipe.title), 'Test title')
        self.assertEqual(str(recipe.slug), 'test-title')
        self.assertEqual(str(recipe.intro), 'Test intro')
        self.assertEqual(str(recipe.ingredients), 'Test ingredients')
        self.assertEqual(str(recipe.directions), 'Test directions')
        self.assertEqual(str(recipe.outro), 'Test outro')
        self.assertEqual(str(recipe.excerpt), 'Test excerpt')
        self.assertEqual(str(recipe.created), '2022-10-10 00:00:00+00:00')
        self.assertEqual(str(recipe.updated), '2022-10-10 00:00:00+00:00')
        self.assertFalse(recipe.published)
        self.assertEqual(str(recipe), recipe_string)


class TestComments(TestCase):
    """
    Test comment model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.save()
        self.recipe_a = Recipe.objects.create(
            title='Test Recipe',
            intro='Test intro',
            ingredients='Test ingredients',
            directions='Test directions',
            excerpt='Test excerpt',
        )
        self.recipe_a.save()

    def test_comment(self):
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            comment = Comment.objects.create(
                user=self.user,
                recipe=self.recipe_a,
                content='Test content',
                added_on=mocked,
                edited_on=mocked,
            )
        comment_string = 'Test content'
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.recipe, self.recipe_a)
        self.assertEqual(str(comment.content), 'Test content')
        self.assertEqual(str(comment.added_on), '2022-10-10 00:00:00+00:00')
        self.assertEqual(str(comment.edited_on), '2022-10-10 00:00:00+00:00')
        self.assertFalse(comment.approved)


class TestSubmittedRecipe(TestCase):
    """
    Test user submitted recipe model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.save()

    def test_submitted_recipe(self):
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            recipe = SubmittedRecipe.objects.create(
                user=self.user,
                recipe_title='Test title',
                ingredients='Test ingredients',
                directions='Test directions',
                notes='Test notes',
                submitted_on=mocked,
                edited_on=mocked,
            )
        recipe_string = 'Test title'
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(str(recipe.recipe_title), 'Test title')
        self.assertEqual(str(recipe.ingredients), 'Test ingredients')
        self.assertEqual(str(recipe.directions), 'Test directions')
        self.assertEqual(str(recipe.notes), 'Test notes')
        self.assertEqual(str(recipe.submitted_on), '2022-10-10 00:00:00+00:00')
        self.assertEqual(str(recipe.edited_on), '2022-10-10 00:00:00+00:00')
        self.assertFalse(recipe.published)
        self.assertEqual(str(recipe.recipe_title), recipe_string)
