from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from management.mixins import StaffRequiredMixin
from .models import Recipe, Comment, SubmittedRecipe


class RecipeList(generic.ListView):
    model = Recipes
    template_name = 'recipes/recipes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipes.objects.filter(published=True).order_by('-added_on')
        return queryset


class ViewRecipe(StaffRequiredMixin, View):
    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('-added_on')
        template_name = 'recipes/recipe_detail.html'
        context - {
            'recipe': recipe,
            'comments': comments,
            'commented': False,
            'form': CommentForm(),
        }
        return render(request, template_name, context)

    def post(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('-added_on')
        template_name = 'recipes/recipe_detail.html'
        form = CommentForm(data=request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                form.instance.user = request.user.userprofile
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.save()
            else:
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.save()
        else:
            form = CommentForm()

        context = {
            'recipe': recipe,
            'comments': comments,
            'reviewed': True,
            'form': form,
        }
        return render(request, template_name, context)


class CreateRecipe(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Recipes
    fields = ('title', 'excerpt', 'ingredients', 'directions',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/management/'
    success_message = 'Your recipe was created'


class UpdateRecipe(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Recipes
    fields = ('title', 'excerpt', 'ingredients', 'directions',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/management/'
    success_message = 'Your recipe was updated'


class DeleteRecipe(StaffRequiredMixin, DeleteView):
    model = Recipes
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'
