from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=40, unique=True)
    intro = models.TextField()
    ingredients = models.TextField()
    direction = models.TextField()
    outro = models.TextField(null=True, blank=True)
    excerpt = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)


class Comment(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    recipe_title = models.CharField(max_length=140)
    ingredients = models.TextField()
    directions = models.TextField()
    notes = models.TextField(null=True, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.recipe_title
