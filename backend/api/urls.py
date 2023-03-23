"""Set your api URLs here."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, FollowViewSet
from .views import (RecipeViewSet, TagViewSet,
                    IngredientViewSet, FavoriteViewSet,
                    ShoppingCartViewSet)

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shoppingcart')
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowViewSet,
    basename='subscribe')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
