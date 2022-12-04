from django.urls import path

from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipes_list'),
    path('recipe/', views.ViewRecipe.as_view(), name='recipe'),
    path('add_recipe/', views.CreateRecipe.as_view(), name='add_recipe'),
    path('edit_recipe/', views.UpdateRecipe.as_view(), name='edit_recipe'),
    path('delete_recipe/', views.DeleteRecipe.as_view(), name='delete_recipe'),
    path('edit_comment/', views.EditComment.as_view(), name='edit_comment'),
    path('delete_comment/', views.DeleteComment.as_view(),
         name='delete_comment'),
    path('submit_recipe/', views.SubmitRecipe.as_view(), name='submit_recipe'),
    path('edit_submitted/', views.EditSubmittedRecipe.as_view(),
         name='edit_submitted'),
    path('delete_submitted/', views.DeleteSubmittedRecipe.as_view(),
         name='delete_submitted'),
]
