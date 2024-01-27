from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя продукта')
    usage_count = models.IntegerField(default=0, verbose_name='Кол-во использований')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    products = models.ManyToManyField(Product, through='ProductToRecipe')

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class ProductToRecipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        # create PK with two (or more) fields
        unique_together = ('product', 'recipe')
        verbose_name = "Продукты - рецепты"
        verbose_name_plural = "Продукты - рецепты"
