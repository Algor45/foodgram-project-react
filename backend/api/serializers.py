"""Write your api app serializers here."""
from django.contrib.auth import get_user_model
from recipes.models import (Recipe, Tag, Ingredient, Cart, Favorite,
                            RecipeIngredient)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Tag."""

    class Meta:
        """Meta настройки сериалайзера для модели Tag."""

        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Ingredient."""

    class Meta:
        """Meta настройки сериалайзера для модели Ingredient."""

        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели RecipeIngredient."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """Meta настройки сериалайзера для модели RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAddSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели RecipeIngredient."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        """Meta настройки сериалайзера для модели RecipeIngredient."""

        model = Ingredient
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериалайзер списочного представления для модели Recipe."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, read_only=True,
                                             source='recipe')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    class Meta:
        """
        Meta настройки сериалайзера списочного представления.

        Для модели Recipe.
        """

        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        """Метод для получения свойства is_favorited."""
        return (self.context.get('request').user.is_authenticated
                and Favorite.objects.filter(
                    user=self.context.get('request').user,
                    recipe=obj
        ).exists())

    def get_is_in_shopping_cart(self, obj):
        """Метод для получения свойства is_in_shopping_cart."""
        return (self.context.get('request').user.is_authenticated
                and Cart.objects.filter(
                    user=self.context.get('request').user,
                    recipe=obj
        ).exists())


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Recipe."""

    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientAddSerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Meta настройки сериалайзера для модели Recipe."""
        model = Recipe
        fields = ('__all__')

    def validate(self, data):
        """Метод валидации."""
        ingredients = data.get('ingredients')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(
                    id=ingredient['id']).exists():
                raise serializers.ValidationError({
                    'ingredients': f'Ингредиента с id - {ingredient["id"]} нет'
                })
        if len(ingredients) != len(set([item['id'] for item in ingredients])):
            raise serializers.ValidationError(
                'Ингредиент должен быть уникальным.')
        tags = data.get('tags')
        if len(tags) != len(set([item for item in tags])):
            raise serializers.ValidationError({
                'tags': 'Тэгдолжен быть уникальным.'})
        return data

    def create_ingredients(self, ingredients, recipe):
        """Метод для создания Ингредиентов."""
        for ingredient in ingredients:
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),)
            ])

    def create(self, validated_data):
        """Переопределение метода create."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Переопределение метода update."""
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Переопределение метода to_representation."""
        return RecipeListSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Favorite."""

    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        """Meta настройки сериалайзера для модели Favorite."""
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        """Валидация сериалайзера."""
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Favorite.objects.filter(user=user,
                                   recipe=recipe).exists():
            raise serializers.ValidationError({
                'Рецепт уже добавлен в избранное.'})
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Cart."""

    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        """Meta настройки сериалайзера для модели Cart."""
        model = Cart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        """Валидация сериалайзера."""
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Cart.objects.filter(user=user,
                               recipe=recipe).exists():
            raise serializers.ValidationError({
                'Рецепт уже добавлен в корзину.'})
        return data
