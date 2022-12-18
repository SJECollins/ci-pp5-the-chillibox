from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Recipe(models.Model):
    """
    Recipe model for use by staff
    User field included but currently not necessary as only staff publish
    recipes and field not used for crediting at the moment. Future proofing
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=40, unique=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True,
                              help_text='Optionally upload an image')
    intro = models.TextField(help_text='Short introduction of the recipe. If \
                             using user submitted recipe, please remember to \
                             credit the user.')
    ingredients = models.TextField(help_text='Place ingredients in \
                                   &lt;li&gt;&lt;/li&gt; tags')
    directions = models.TextField(help_text='Place directions in \
                                  &lt;li&gt;&lt;/li&gt; tags')
    outro = models.TextField(null=True, blank=True, help_text='Optional. A \
                             short outro for the recipe.')
    excerpt = models.TextField(help_text='Summary to display on recipe list.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save to slugify title for slug field
        """
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)


class Comment(models.Model):
    """
    Comment model
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='comments')
    content = models.TextField(max_length=280)
    added_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class SubmittedRecipe(models.Model):
    """
    Submitted recipe model for use by non-staff users
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    recipe_title = models.CharField(max_length=140)
    ingredients = models.TextField()
    directions = models.TextField()
    notes = models.TextField(null=True, blank=True, help_text='Please include \
                             any notes or insights you would like included.')
    submitted_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.recipe_title
