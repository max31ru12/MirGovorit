from django.contrib import admin
from django.urls import path
from .views import AddProductToRecipe, cook_recipe_view, recipes_without_product_view


urlpatterns = [
    path('add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>', AddProductToRecipe.as_view()),
    path('cook_recipe/<int:recipe_id>/', cook_recipe_view),
    path('show_recipes_without_product/<int:product_id>/', recipes_without_product_view),
]