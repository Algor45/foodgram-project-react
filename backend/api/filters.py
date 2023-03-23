"""Write your api app filters here."""
import django_filters
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для IngredientViewSet."""

    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        """Meta модуль фильтра IngredientFilter."""

        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для RecipeViewSet."""

    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',)
    is_favorited = django_filters.filters.BooleanFilter(
        method='get_is_favorited')
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        """Meta модуль фильтра RecipeFilter."""

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        """get метод is_favorited для RecipeViewSet."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """get метод is_in_shopping_cart для RecipeViewSet."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(recipe_cart__user=user)
        return queryset
