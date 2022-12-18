import datetime
import pytz
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Category, Product, Variant
from profiles.models import Reviews
from recipes.models import Recipe, Comment, SubmittedRecipe


class TestManagementViewsNotLoggedIn(TestCase):
    """
    Test views when user is not logged in.
    """
    def setUp(self):
        """
        Setup for testing
        """
        self.category_a = Category.objects.create(
            name='Test Category',
            slug='test-cat'
        )
        self.category_a.save()
        self.product_a = Product.objects.create(
            category=self.category_a,
            name='Test Pepper',
            slug='test-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()

    def test_dashboard(self):
        """
        Test get management dashboard if not logged in.
        Should redirect to login.
        """
        response = self.client.get('/management/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/management/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_add_variant(self):
        """
        Test adding variant if not logged in.
        """
        slug = self.product_a.slug
        response = self.client.get(
            reverse('management:add_variant', args=[slug]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/add_variant/test-pepper',  # noqa
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_variant(self):
        """
        Test editing variant if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_variant', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/edit_variant/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_variant(self):
        """
        Test deleting variant if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_variant', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/delete_variant/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_add_product(self):
        """
        Testing adding product if not logged in.
        """
        response = self.client.get('/management/add_product/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/add_product/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_product(self):
        """
        Testing editing product if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_product', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/edit_product/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_product(self):
        """
        Test deleting product if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_product', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/delete_product/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_user_reviews(self):
        """
        Test viewing user reviews if not logged in.
        """
        response = self.client.get('/management/user_reviews/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/user_reviews/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_remove_review(self):
        """
        Test removing user reviews if not logged in.
        """
        review = self.review_a.id
        response = self.client.get(reverse('management:remove_review',
                                   args=[review]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/remove_review/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_update_stock(self):
        """
        Test updating stock if not logged in.
        """
        id = self.variant_a.id
        response = self.client.get(reverse('management:update_stock',
                                   args=[id]))
        self.assertRedirects(
            response, '/accounts/login/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_recipes_list(self):
        """
        Test viewing  if not logged in.
        """
        response = self.client.get('/management/recipes/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/recipes/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_comment_list(self):
        """
        Test viewing user reviews if not logged in.
        """
        response = self.client.get('/management/recipe_comments/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/recipe_comments/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_user_recipes_list(self):
        """
        Test viewing submitted recipes if not logged in.
        """
        response = self.client.get('/management/user_recipes/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/user_recipes/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)


class TestManagementViewsLoggedIn(TestCase):
    """
    Test views when user is logged in but not staff.
    """
    def setUp(self):
        """
        Setup for testing
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = False
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.category_a = Category.objects.create(
            name='Test Category',
            slug='test-cat'
        )
        self.category_a.save()
        self.product_a = Product.objects.create(
            category=self.category_a,
            name='Test Pepper',
            slug='test-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()
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

    def test_dashboard(self):
        """
        Test get management dashboard if logged in but is_staff is false.
        Should raise 403
        """
        response = self.client.get('/management/', follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_add_variant(self):
        """
        Test adding variant if logged in but is_staff is false.
        """
        slug = self.product_a.slug
        response = self.client.get(
            reverse('management:add_variant', args=[slug]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_variant(self):
        """
        Test editing variant if logged in but is_staff is false.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_variant', args=[id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_variant(self):
        """
        Test deleting variant if logged in but is_staff is false.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_variant', args=[id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_add_product(self):
        """
        Testing adding product if logged in but is_staff is false.
        """
        response = self.client.get('/management/add_product/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_product(self):
        """
        Testing editing product if logged in but is_staff is false.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_product', args=[id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_product(self):
        """
        Test deleting product if logged in but is_staff is false.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_product', args=[id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_user_reviews(self):
        """
        Test viewing user reviews if logged in but is_staff is false.
        """
        response = self.client.get('/management/user_reviews/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_remove_review(self):
        """
        Test removing user reviews if logged in but is_staff is false.
        """
        review = self.review_a.id
        response = self.client.get(reverse('management:remove_review',
                                   args=[review]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_update_stock(self):
        """
        Test updating stock if logged in but is_staff is false.
        Function redirects to login, which will redirect to profile if logged
        in.
        """
        id = self.variant_a.id
        response = self.client.get(reverse('management:update_stock',
                                   args=[id]), follow=True)
        self.assertRedirects(
            response, '/profiles/profile/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_recipes_list(self):
        """
        Test viewing  if logged in but is_staff is false.
        """
        response = self.client.get('/management/recipes/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_comment_list(self):
        """
        Test viewing user reviews if logged in but is_staff is false.
        """
        response = self.client.get('/management/recipe_comments/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_user_recipes_list(self):
        """
        Test viewing submitted recipes if logged in but is_staff is false.
        """
        response = self.client.get('/management/user_recipes/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_approve_review_not_staff(self):
        """
        Test trying to approve review if not staff
        """
        pk = self.review_a.id
        response = self.client.get(reverse('management:approve_review',
                                   args=[pk]), follow=True)
        self.assertRedirects(response, '/profiles/profile/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_publish_recipe_not_staff(self):
        """
        Test trying to publish recipe if not staff
        """
        pk = self.recipe_a.id
        response = self.client.get(reverse('management:publish_recipe',
                                   args=[pk]), follow=True)
        self.assertRedirects(response, '/profiles/profile/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_approve_comment_not_staff(self):
        """
        Test trying to approve comment if not staff
        """
        pk = self.comment_a.id
        response = self.client.get(reverse('management:approve_comment',
                                   args=[pk]), follow=True)
        self.assertRedirects(response, '/profiles/profile/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_publish_submitted_recipe_not_staff(self):
        """
        Test trying to publish submitted recipe if not staff
        """
        pk = self.submitted_recipe.id
        response = self.client.get(reverse('management:publish_submitted',
                                   args=[pk]), follow=True)
        self.assertRedirects(
            response, '/profiles/profile/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)


class TestManagementViewsIsStaff(TestCase):
    """
    Test views when user is logged in and is staff.
    """
    def setUp(self):
        """
        Setup for testing
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.category_a = Category.objects.create(
            name='Test Category',
            slug='test-cat'
        )
        self.category_a.save()
        self.product_a = Product.objects.create(
            category=self.category_a,
            name='Test Pepper',
            slug='test-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()
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

    def test_dashboard(self):
        """
        Test get management dashboard if logged in and is staff.
        Should render dashboard.
        """
        response = self.client.get('/management/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/dashboard.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_add_variant(self):
        """
        Test adding variant if logged in and is staff.
        """
        slug = self.product_a.slug
        response = self.client.get(
            reverse('management:add_variant', args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/dashboard_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_variant(self):
        """
        Test editing variant if logged in and is staff.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_variant', args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/dashboard_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_variant(self):
        """
        Test deleting variant if logged in and is staff.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_variant', args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_add_product(self):
        """
        Testing adding product if logged in and is staff.
        """
        response = self.client.get('/management/add_product/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/dashboard_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_product(self):
        """
        Testing editing product if logged in and is staff.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_product', args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/dashboard_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_product(self):
        """
        Test deleting product if logged in and is staff.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_product', args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_user_reviews(self):
        """
        Test viewing user reviews if logged in and is staff.
        """
        response = self.client.get('/management/user_reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/user_reviews.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_remove_review(self):
        """
        Test removing user reviews if logged in and is staff.
        """
        review = self.review_a.id
        response = self.client.get(reverse('management:remove_review',
                                   args=[review]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_update_stock(self):
        """
        Test updating stock if logged in and is staff.
        """
        id = self.variant_a.id
        response = self.client.get(reverse('management:update_stock',
                                   args=[id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/update_stock.html')

    def test_update_stock_updating(self):
        """
        Test updating stock if logged in and is staff, post.
        """
        id = self.variant_a.id
        data = {
            'current_stock': 20,
        }
        response = self.client.post(reverse('management:update_stock',
                                    args=[id]), data)
        self.assertEqual(response.status_code, 204)

    def test_recipes_list(self):
        """
        Test viewing  if logged in and is_staff.
        """
        response = self.client.get('/management/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/recipes.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_comment_list(self):
        """
        Test viewing user reviews if logged in and is_staff.
        """
        response = self.client.get('/management/recipe_comments/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/recipe_comments.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_user_recipes_list(self):
        """
        Test viewing submitted recipes if logged in and is_staff.
        """
        response = self.client.get('/management/user_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/user_recipes.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_approve_review(self):
        """
        Testing approving review if is staff
        """
        pk = self.review_a.id
        data = {
            'approved': True,
        }
        response = self.client.get(reverse('management:approve_review',
                                   args=[pk]), data)
        self.assertRedirects(
            response, '/management/user_reviews/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_publish_recipe(self):
        """
        Testing publishing recipe if is staff
        """
        pk = self.recipe_a.id
        data = {
            'published': True,
        }
        response = self.client.get(reverse('management:publish_recipe',
                                   args=[pk]), data)
        self.assertRedirects(
            response, '/management/recipes/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_approve_comment(self):
        """
        Testing approving comment if is staff
        """
        pk = self.comment_a.id
        data = {
            'approved': True,
        }
        response = self.client.get(reverse('management:approve_comment',
                                   args=[pk]), data)
        self.assertRedirects(
            response, '/management/recipe_comments/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_publish_submitted_recipe(self):
        """
        Testing publishing submitted recipe if is staff
        """
        pk = self.submitted_recipe.id
        data = {
            'published': True,
        }
        response = self.client.get(reverse('management:publish_submitted',
                                   args=[pk]), data)
        self.assertRedirects(
            response, '/management/user_recipes/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)
