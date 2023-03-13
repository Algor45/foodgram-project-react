"""Write here Admin settings for recipes app."""
from django.contrib import admin

from .models import (Cart, Favorite, Tag, Recipe,
                     Ingredient, RecipeIngredient, RecipeTag)

EMPTY_DISPLAY = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Recipe."""

    list_display = ('id', 'name', 'author', 'text',
                    'cooking_time', 'get_ingredients', 'get_tags',
                    'pub_date', 'favorite_count')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = EMPTY_DISPLAY

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        """Метод для получения Тэгов."""
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        """Метод для получения ингредиентов."""
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])

    def favorite_count(self, obj):
        """Метод для получения подсчета избранного."""
        return obj.favorite.count()


class TagAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Tag."""

    list_display = (
        'id', 'name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    empty_value_display = EMPTY_DISPLAY


class IngredientAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Ingredient."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = EMPTY_DISPLAY


class RecipeIngredientAdmin(admin.ModelAdmin):
    """Настройки администратора для модели RecipeIngredient."""

    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = EMPTY_DISPLAY


class FavoriteAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Favorite."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EMPTY_DISPLAY


class CartAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Cart."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EMPTY_DISPLAY


class RecipeTagAdmin(admin.ModelAdmin):
    """Настройки администратора для модели RecipeTag."""

    list_display = ('id', 'recipe', 'tag')
    search_fields = ('tag', 'recipe',)
    list_filter = ('tag', 'recipe',)
    empty_value_display = EMPTY_DISPLAY


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
