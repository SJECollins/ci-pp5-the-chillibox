from django.contrib import admin

from .models import Recipe, Comment, SubmittedRecipe

# Registering models with admin
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(SubmittedRecipe)
