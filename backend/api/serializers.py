"""Write your api app serializers here."""
from recipes.models import (Recipe, Tag, Ingredient, Cart, Favorite,
                            RecipeIngredient)
from drf_extra_fields.fields import Base64ImageField
from users.serializers import UserSerializer
from rest_framework import serializers


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


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериалайзер списочного представления для модели Recipe."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Meta настройки сериалайзера списочного представления.

        Для модели Recipe.
        """

        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_ingredients(self, obj):
        """Метод для получения ингредиентов."""
        ings = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ings, many=True).data

    def get_is_favorited(self, obj):
        """Метод для получения свойства is_favorited."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод для получения свойства is_in_shopping_cart."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, recipe=obj).exists()


class IngredientAddSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        """Meta настройки сериалайзера для модели RecipeIngredient."""

        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Recipe."""

    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientAddSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        """Meta настройки сериалайзера для модели Recipe."""

        fields = ('id', 'tags', 'author', 'ingredients',
                  'name',  'image', 'text',
                  'cooking_time')
        model = Recipe

    def validate(self, data):
        """Метод валидации."""
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for item in ingredients:
            curr_ingr = item['id']
            if curr_ingr in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиент должен быть уникаленым.'
                )
            ingredients_list.append(curr_ingr)
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'У рецепта должен быть хотя бы 1 тэг.'
            )
        for curr_tag in tags:
            if not Tag.objects.filter(name=curr_tag).exists():
                raise serializers.ValidationError(
                    f'Не существует тэга: {curr_tag}'
                )
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1.'
            )
        return data

    def validate_ingredients(self, ingredients):
        """Метод валидации ингредиентов."""
        if not ingredients:
            raise serializers.ValidationError(
                'В рецепте должен быть указан хотя бы 1 ингредиент.'
            )
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть меньше 1.'
                )
        return ingredients

    def create_tags(self, tags, recipe):
        """Метод для создания Тэгов."""
        for tag in tags:
            recipe.tags.add(tag)

    def create_ingredients(self, ingredients, recipe):
        """Метод для создания Ингредиентов."""
        for item in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=item.get('id'),
                amount=item.get('amount'))

    def create(self, validated_data):
        """Переопределение метода create."""
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
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


class FavCartRecipeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Recipe.

    С сокращенным отображением.
    """

    class Meta:
        """
        Meta настройки сериалайзера для модели Recipe.

        С сокращенным отображением.
        """

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
