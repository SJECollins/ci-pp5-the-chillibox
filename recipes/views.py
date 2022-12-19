from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from management.mixins import StaffRequiredMixin
from .models import Recipe, Comment, SubmittedRecipe
from .forms import CommentForm


class RecipeList(generic.ListView):
    """
    Recipe list view
    Generic list view, paginated
    Queryset filter returns published recipes by date created
    """
    model = Recipe
    template_name = 'recipes/recipes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.filter(published=True).order_by('-created')
        return queryset


class ViewRecipe(View):
    """
    Recipe view
    Generic view, using CommentForm from forms.py
    """
    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('-added_on')
        template_name = 'recipes/recipe_detail.html'
        context = {
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
                form.instance.user = request.user
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.save()
            else:
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.save()
        else:
            form = CommentForm()

        context = {
            'recipe': recipe,
            'comments': comments,
            'form': form,
            'commented': True,
        }
        return render(request, template_name, context)


class CreateRecipe(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create Recipe view
    CreateView using Recipe model, specify fields
    StaffRequiredMixin as user must be registered and staff, otherwise
    redirects user
    SuccessMessageMixin to display success message when form submitted
    """
    model = Recipe
    fields = ('title', 'image', 'intro', 'excerpt', 'ingredients',
              'directions', 'outro',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/management/recipes/'
    success_message = 'Your recipe was created.'


class UpdateRecipe(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update recipe view
    UpdateView using Recipe model
    StaffRequiredMixin as user must be registered and staff, otherwise
    redirects user
    SuccessMessageMixin to display success message when form submitted
    """
    model = Recipe
    fields = ('title', 'image', 'intro', 'excerpt', 'ingredients',
              'directions', 'outro',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/management/recipes/'
    success_message = 'Your recipe was updated.'


class DeleteRecipe(StaffRequiredMixin, DeleteView):
    """
    Delete recipe view
    DeleteView using Recipe model
    StaffRequiredMixin as user must be registered and staff, otherwise
    redirects user
    """
    model = Recipe
    template_name = 'management/confirm_delete.html'
    success_url = '/management/recipes/'


class EditComment(LoginRequiredMixin, UpdateView):
    """
    Edit comment view
    UpdateView - doesn't use CommentForm in forms.py, uses Comment model
    LoginRequiredMixin as only registered users can edit their comments
    """
    model = Comment
    fields = ('content',)
    template_name = 'recipes/comment_form.html'
    success_url = '/recipes/'


class DeleteComment(LoginRequiredMixin, DeleteView):
    """
    Delete comment view
    DeleteView using Comment model
    LoginRequiredMixin as only registered users and staff can delete comments
    """
    model = Comment
    template_name = 'management/confirm_delete.html'
    success_url = '/recipes/'


class SubmitRecipe(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Submit recipe view
    CreateView using SubmittedRecipe view
    LoginRequiredMixin as only registered users can submit recipes
    SuccessMessageMixin to display success message when user submits recipe
    """
    model = SubmittedRecipe
    fields = ('recipe_title', 'ingredients', 'directions', 'notes',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/profiles/user_recipes/'
    success_message = 'Your recipe has been submitted.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SubmitRecipe, self).form_valid(form)


class EditSubmittedRecipe(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit submitted recipe view
    UpdateView using SubmittedRecipe model
    LoginRequiredMixin as only registered users can submit and edit recipes
    SuccessMessageMixin to display success message when user edits recipe
    """
    model = SubmittedRecipe
    fields = ('recipe_title', 'ingredients', 'directions', 'notes',)
    template_name = 'recipes/recipe_form.html'
    success_url = '/profiles/user_recipes/'
    success_message = 'Your recipe has been edited.'


class DeleteSubmittedRecipe(LoginRequiredMixin, DeleteView):
    """
    Delete submitted recipe view
    DeleteView using SubmittedRecipe
    LoginRequiredMixin as only registered users and staff can delete submitted
    recipes
    """
    model = SubmittedRecipe
    template_name = 'management/confirm_delete.html'
    success_url = '/profiles/user_recipes/'
