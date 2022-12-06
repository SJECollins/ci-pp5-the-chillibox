from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


from .models import Recipe, Comment, SubmittedRecipe


class TestRecipes(TestCase):
    """
    Test views for recipe app if not logged in.
    """
    def setUp(self):
        self.recipe_a = Recipe.objects.create(
            title='Test Recipe',
            intro='Test intro',
            ingredients='Test ingredients',
            directions='Test directions',
            excerpt='Test excerpt',
        )
        self.recipe_a.save()
        self.comment_a = Comment.objects.create(
            recipe=self.recipe_a,
            content='Test comment',
        )
        self.comment_a.save()
        self.submitted_recipe = SubmittedRecipe.objects.create(
            recipe_title='Test Title',
            ingredients='Test ingredients',
            directions='Test directions'
        )
        self.submitted_recipe.save()

    def test_recipe_list(self):
        """
        Test recipe list view.
        Does not require user to be logged in or staff.
        """
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_recipe_detail(self):
        """
        Test recipe detail view.
        Does not require user to be logged in or staff.
        """
        slug = self.recipe_a.slug
        response = self.client.get(reverse('recipes:recipe', args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_add_recipe_view(self):
        """
        Test add recipe view.
        Requires logged in and is_staff.
        """
        response = self.client.get('/recipes/add_recipe/')
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/add_recipe/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_recipe_view(self):
        """
        Test edit recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:edit_recipe', args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/edit_recipe/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_recipe_view(self):
        """
        Test delete recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:delete_recipe', args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/delete_recipe/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_comment_view(self):
        """
        Test edit comment view.
        Requires logged in.
        """
        pk = self.comment_a.pk
        response = self.client.get(reverse('recipes:edit_comment', args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/edit_comment/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_comment_view(self):
        """
        Test delete comment view.
        Requires logged in.
        """
        pk = self.comment_a.pk
        response = self.client.get(reverse('recipes:delete_comment',
                                   args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/delete_comment/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_submit_recipe_view(self):
        """
        Test submit recipe view.
        Requires logged in.
        """
        response = self.client.get('/recipes/submit_recipe/')
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/submit_recipe/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_user_recipe_view(self):
        """
        Test edit user recipe view.
        Requires logged in.
        """
        pk = self.submitted_recipe.pk
        response = self.client.get(reverse('recipes:edit_submitted',
                                   args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/edit_submitted/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_user_recipe_view(self):
        """
        Test delete user recipe view.
        Requires logged in.
        """
        pk = self.submitted_recipe.pk
        response = self.client.get(reverse('recipes:delete_submitted',
                                   args=[pk]))
        self.assertRedirects(
            response, '/accounts/login/?next=/recipes/delete_submitted/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)


class TestRecipesLoggedIn(TestCase):
    """
    Test views for recipe app logged in but not is_staff.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = False
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.recipe_a = Recipe.objects.create(
            title='Test Recipe',
            intro='Test intro',
            ingredients='Test ingredients',
            directions='Test directions',
            excerpt='Test excerpt',
        )
        self.recipe_a.save()
        self.comment_a = Comment.objects.create(
            recipe=self.recipe_a,
            content='Test comment',
        )
        self.comment_a.save()
        self.submitted_recipe = SubmittedRecipe.objects.create(
            recipe_title='Test Title',
            ingredients='Test ingredients',
            directions='Test directions'
        )
        self.submitted_recipe.save()

    def test_add_recipe_view(self):
        """
        Test add recipe view.
        Requires logged in and is_staff.
        """
        response = self.client.get('/recipes/add_recipe/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_recipe_view(self):
        """
        Test edit recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:edit_recipe', args=[pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_recipe_view(self):
        """
        Test delete recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:delete_recipe', args=[pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_comment_view(self):
        """
        Test edit comment view.
        Requires logged in.
        """
        pk = self.comment_a.pk
        response = self.client.get(reverse('recipes:edit_comment', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/comment_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_comment_view(self):
        """
        Test delete comment view.
        Requires logged in.
        """
        pk = self.comment_a.pk
        response = self.client.get(reverse('recipes:delete_comment',
                                   args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_submit_recipe_view(self):
        """
        Test submit recipe view.
        Requires logged in.
        """
        response = self.client.get('/recipes/submit_recipe/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_user_recipe_view(self):
        """
        Test edit user recipe view.
        Requires logged in.
        """
        pk = self.submitted_recipe.pk
        response = self.client.get(reverse('recipes:edit_submitted',
                                   args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_user_recipe_view(self):
        """
        Test delete user recipe view.
        Requires logged in.
        """
        pk = self.submitted_recipe.pk
        response = self.client.get(reverse('recipes:delete_submitted',
                                   args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')


class TestRecipesLoggedIn(TestCase):
    """
    Test views for recipe app logged in but not is_staff.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.recipe_a = Recipe.objects.create(
            title='Test Recipe',
            intro='Test intro',
            ingredients='Test ingredients',
            directions='Test directions',
            excerpt='Test excerpt',
        )
        self.recipe_a.save()
        self.comment_a = Comment.objects.create(
            recipe=self.recipe_a,
            content='Test comment',
        )
        self.comment_a.save()
        self.submitted_recipe = SubmittedRecipe.objects.create(
            recipe_title='Test Title',
            ingredients='Test ingredients',
            directions='Test directions'
        )
        self.submitted_recipe.save()

    def test_add_recipe_view(self):
        """
        Test add recipe view.
        Requires logged in and is_staff.
        """
        response = self.client.get('/recipes/add_recipe/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_recipe_view(self):
        """
        Test edit recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:edit_recipe', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_recipe_view(self):
        """
        Test delete recipe view.
        Requires logged in and is_staff.
        """
        pk = self.recipe_a.pk
        response = self.client.get(reverse('recipes:delete_recipe', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
