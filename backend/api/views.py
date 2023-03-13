"""Set your api Views here."""
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.models import (Recipe, Tag, Ingredient, Cart, Favorite,
                            RecipeIngredient)
from users.models import CustomUser
from .serializers import (TagSerializer, RecipeSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          FavCartRecipeSerializer)
from .filters import IngredientFilter, RecipeFilter
from .permissions import AuthorPermissionOrReadOnly
from .pagintaion import CustomPagination
from rest_framework import mixins, viewsets
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


def add_or_delete_method(request, pk, model):
    """
    Метод для добавления и удаления.

    Для Favorite и Cart.
    """
    user = get_object_or_404(CustomUser, username=request.user)
    recipe = get_object_or_404(Recipe, pk=pk)

    if str(request.method) == 'POST':
        model.objects.get_or_create(user=user, recipe=recipe)
        recipe_serializer = FavCartRecipeSerializer(recipe)
        return Response(recipe_serializer.data, status=HTTP_201_CREATED)
    item = get_object_or_404(model, user=user, recipe=recipe)
    item.delete()
    return Response(status=HTTP_204_NO_CONTENT)


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Mixin RetrieveList."""

    pass


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для модели Recipe и сериалайзеров."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorPermissionOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Выбор сериалайзера в зависимости от типа запроса."""
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавить или удалить из избранного."""
        return add_or_delete_method(request, pk, Favorite)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавить или удалить из корзины."""
        return add_or_delete_method(request, pk, Cart)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Метод для скачивания ингредиентов в корзине в txt."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )
        shopping_cart = '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = 'cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(RetrieveListViewSet):
    """Viewset для модели Tag и TagSerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class IngredientViewSet(RetrieveListViewSet):
    """Viewset для модели Ingredient и IngredientSerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
