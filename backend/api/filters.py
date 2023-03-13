"""Write your api app filters here."""
import django_filters
from recipes.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для IngredientViewSet."""

    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        """Meta модуль фильтра IngredientFilter."""

        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для RecipeViewSet."""

    tags = django_filters.filters.AllValuesMultipleFilter(
        field_name='tags__slug')
    is_favorited = django_filters.filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        """Meta модуль фильтра RecipeFilter."""

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр метод is_favorited для RecipeViewSet."""
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр метод is_in_shopping_cart для RecipeViewSet."""
        if value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset
