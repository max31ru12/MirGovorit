from django.db.models import QuerySet, Manager, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import ProductToRecipe, Recipe, Product


def prefetch_decorator(func: callable):
    def wrapper(query: Manager, relation: str = None, *args, **kwargs):
        if relation:
            query = query.prefetch_related(relation)
        return func(query, *args, **kwargs)

    return wrapper


def distinct_decorator(func: callable):
    def wrapper(query: Manager, distinct: bool = False, *args, **kwargs):
        if distinct:
            return func(query, *args, **kwargs).distinct()
        return func(query, *args, **kwargs)
    return wrapper


""" Base logic """


@distinct_decorator
@prefetch_decorator
def get_all_objects(query: Manager) -> QuerySet:
    """ Function gets all objects from Model.Manager """
    return query.all()


@prefetch_decorator
def get_object_by_id(query: Manager, obj_id: int) -> QuerySet:
    """ Function gets object by id from Model.Manager """
    return query.get(id=obj_id)


@distinct_decorator
@prefetch_decorator
def filter_objects(query: Manager, condition=None, **kwargs) -> QuerySet:
    """ Function filters objects by provided condition and kwargs"""
    if condition:
        return query.filter(condition, **kwargs)
    return query.filter(**kwargs)


""" Business logic for the cookbook """


def select_recipes_without_product(query: Manager, product_id: int) -> QuerySet:
    """ Function to get less than 10 or without product """
    condition = Q(~Q(products__id=product_id)) | (Q(producttorecipe__weight__lt=10) & Q(products__id=product_id))
    recipes = filter_objects(query,
                             relation='products',
                             distinct=True,
                             condition=condition)
    return recipes


def add_product_to_recipe(recipe_id: int, product_id: int, weight: int) -> HttpResponse:
    """ Functions adds product to recipe or updates product's weight """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    product = get_object_or_404(Product, id=product_id)
    # "defaults" separates field "weight" from search fields
    recipe_product, created = ProductToRecipe.objects.get_or_create(recipe=recipe,
                                                                    product=product,
                                                                    defaults={'weight': weight})
    if not created:
        recipe_product.weight = weight
        recipe_product.save()
        return HttpResponse("Successfully updated weight of product")
    return HttpResponse("Successfully added product to recipe")
