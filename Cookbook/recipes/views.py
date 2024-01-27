from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .services import get_object_by_id, select_recipes_without_product, add_product_to_recipe
from django.views.generic import TemplateView


class AddProductToRecipe(TemplateView):

    def get(self, request, recipe_id: int, product_id: int, weight: int, *args, **kwargs):
        return add_product_to_recipe(recipe_id, product_id, weight)


def cook_recipe_view(request, recipe_id: int):
    recipe = get_object_by_id(Recipe.objects, relation='products', obj_id=recipe_id)
    recipe.products.all().update(usage_count=F('usage_count') + 1)
    return HttpResponse("Success")


def recipes_without_product_view(request, product_id: int):
    recipes = select_recipes_without_product(Recipe.objects, product_id)
    return render(request, 'BasePage.html', context={"recipes": recipes})
