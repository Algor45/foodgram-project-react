"""Set your api Views here."""
from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.models import (Recipe, Tag, Ingredient, Cart, Favorite)
from .serializers import (TagSerializer, RecipeSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)
from .filters import IngredientFilter, RecipeFilter
from .permissions import AuthorPermissionOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.status import (HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS)
User = get_user_model()


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Mixin CreateDestroy."""
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для модели Recipe и сериалайзеров."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AuthorPermissionOrReadOnly)
    filterset_class = RecipeFilter

    def get_queryset(self):
        """Переопределение метода qet_queryset."""
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(cart_recipe__user=self.request.user)
        return Recipe.objects.all()

    def get_serializer_class(self):
        """Выбор сериалайзера в зависимости от типа запроса."""
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        """Переопределение метода perform_create."""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=('get',),
            url_path='download_shopping_cart',
            pagination_class=None)
    def download_shopping_cart(self, request):
        """Метод для скачивания ингредиентов в корзине в txt."""
        user = request.user
        if not user.cart.exists():
            return Response(
                'В корзине нет товаров', status=HTTP_400_BAD_REQUEST)

        text = 'Список покупок:\n\n'
        ingredient_name = 'recipe__recipe__ingredient__name'
        ingredient_unit = 'recipe__recipe__ingredient__measurement_unit'
        recipe_amount = 'recipe__recipe__amount'
        amount_sum = 'recipe__recipe__amount__sum'
        cart = user.cart.select_related('recipe').values(
            ingredient_name, ingredient_unit).annotate(Sum(
                recipe_amount)).order_by(ingredient_name)
        for _ in cart:
            text += (
                f'{_[ingredient_name]} ({_[ingredient_unit]})'
                f' — {_[amount_sum]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для модели Tag и TagSerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для модели Ingredient и IngredientSerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter
    pagination_class = None


class FavoriteViewSet(CreateDestroyViewSet):
    """Viewset для Favorite и FavoriteSerializer."""
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        """Переопределение метода get_queryset."""
        user = self.request.user.id
        return Favorite.objects.filter(user=user)

    def get_serializer_context(self):
        """Переопределение метода get_serializer_context."""
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        """Переопределение метода perform_create."""
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        """Метод для удаления Favorite."""
        user = request.user
        if not user.favorite.select_related(
                'favorite_recipe').filter(
                    recipe_id=recipe_id).exists():
            return Response({'errors': 'Рецепта нет в избранном'},
                            status=HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Favorite,
            user=request.user,
            recipe_id=recipe_id).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Viewset для Cart и ShoppingCartSerializer."""

    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        """Переопределение метода get_queryset."""
        user = self.request.user.id
        return Cart.objects.filter(user=user)

    def get_serializer_context(self):
        """Переопределение метода get_serializer_context."""
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        """Переопределение метода perform_create."""
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        """Метод для удаления Cart."""
        user = request.user
        if not user.cart.select_related(
                'recipe').filter(
                    recipe_id=recipe_id).exists():
            return Response({'errors': 'Рецепта нет в корзине'},
                            status=HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Cart,
            user=request.user,
            recipe=recipe_id).delete()
        return Response(status=HTTP_204_NO_CONTENT)
