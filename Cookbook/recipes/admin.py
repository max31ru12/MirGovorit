from django.contrib import admin
from .models import Recipe, Product, ProductToRecipe


class ProductToRecipeInline(admin.TabularInline):
    model = ProductToRecipe
    extra = 1


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'usage_count')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [ProductToRecipeInline]
    # raw_id_fields = ('products',)
    list_filter = ('name',)


@admin.register(ProductToRecipe)
class ProductToRecipeAdmin(admin.ModelAdmin):
    list_editable = ('weight', )
    list_display = ('id', 'product', 'recipe', 'weight')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'weight':
            kwargs['min_value'] = 0
        return super().formfield_for_dbfield(db_field, request, **kwargs)