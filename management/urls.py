from django.urls import path

from . import views


app_name = 'management'
urlpatterns = [
     path('', views.ProductDashboard.as_view(), name='dashboard'),
     path('add_variant/<slug>', views.AddVariant.as_view(),
          name='add_variant'),
     path('edit_variant/<pk>', views.EditVariant.as_view(),
          name='edit_variant'),
     path('delete_variant/<pk>', views.DeleteVariant.as_view(),
          name='delete_variant'),
     path('add_product/', views.AddProduct.as_view(), name='add_product'),
     path('edit_product/<pk>', views.EditProduct.as_view(),
          name='edit_product'),
     path('delete_product/<pk>', views.DeleteProduct.as_view(),
          name='delete_product'),
     path('user_reviews/', views.ReviewDashboard.as_view(),
          name='user_reviews'),
     path('approve_review/<pk>', views.approve_review, name='approve_review'),
     path('remove_review/<pk>', views.RemoveReview.as_view(),
          name='remove_review'),
     path('update_stock/<pk>', views.update_stock, name='update_stock'),
     path('recipes/', views.RecipeList.as_view(), name='recipes'),
     path('publish_recipe/<pk>', views.publish_recipe, name='publish_recipe'),
     path('recipe_comments/', views.CommentList.as_view(),
          name='recipe_comments'),
     path('approve_comment/<pk>', views.approve_comment,
          name='approve_comment'),
     path('user_recipes/', views.UserRecipeList.as_view(),
          name='user_recipes'),
     path('publish_submitted/<pk>', views.publish_submitted_recipe,
          name='publish_submitted'),
]
