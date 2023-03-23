"""Write here Admin settings for recipes app."""
from django.contrib import admin
from django.db.models import Count

from .models import (Cart, Favorite, Tag, Recipe,
                     Ingredient, RecipeIngredient)

EMPTY_DISPLAY = '-пусто-'


class IngredientAmountAdmin(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Recipe."""

    inlines = (IngredientAmountAdmin,)
    list_display = ('id', 'name', 'author', 'text',
                    'cooking_time', 'pub_date', 'favorite_count')
    search_fields = ('name', 'author', 'tags')
    filter_vertical = ('tags',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = EMPTY_DISPLAY

    def get_queryset(self, request):
        """Переопределение метода get_queryset RecipeAdmin."""
        queryset = super().get_queryset(request)
        return queryset.annotate(
            obj_count=Count("favorite_recipe", distinct=True),
        )

    def favorite_count(self, obj):
        """Метод для получения подсчета избранного."""
        return obj.obj_count


class TagAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Tag."""

    list_display = (
        'id', 'name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_DISPLAY


class IngredientAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Ingredient."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
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


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
