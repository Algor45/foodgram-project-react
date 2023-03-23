"""Set your users serializers here."""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import (UserCreateSerializer,
                                UserSerializer, PasswordSerializer)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Follow
from recipes.models import Recipe

User = get_user_model()


class UserSerializer(UserSerializer):
    """Сериалайзер для модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Meta настройки сериалайзера для модели CustomUser."""

        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        """Метод для получения свойства is_subscribed."""
        return (self.context.get('request').user.is_authenticated
                and Follow.objects.filter(
                    user=self.context.get('request').user,
                    following=obj
        ).exists())


class UserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для регистрации нового пользователя."""

    class Meta:
        """Meta настройки сериалайзера для модели создания пользователя."""

        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )
        required_fields = (
            'email', 'username', 'first_name', 'last_name',
            'password')


class SetPasswordSerializer(PasswordSerializer):
    """Сериалайзер для смены пароля."""

    current_password = serializers.CharField(
        required=True,
        label='Текущий пароль')

    def validate(self, data):
        """Валидация нового пароля."""
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError({
                "new_password": "Пароли не должны совпадать"})
        check_current = check_password(data['current_password'], user.password)
        if check_current is False:
            raise serializers.ValidationError({
                "current_password": "Введен неверный пароль"})
        return data


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для кратких рецептов в подписках."""

    image = Base64ImageField()

    class Meta:
        """Meta настройки сериалайзера кратких рецептов."""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Follow."""

    id = serializers.IntegerField(source='following.id', read_only=True)
    email = serializers.CharField(source='following.email', read_only=True)
    username = serializers.CharField(source='following.username',
                                     read_only=True)
    first_name = serializers.CharField(source='following.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='following.last_name',
                                      read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='following.recipes.count')

    class Meta:
        """Meta настройки сериалайзера модели Follow."""

        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Метод для получения свойства is_subscribed."""
        return Follow.objects.filter(
            user=self.context.get('request').user,
            following=obj.following
        ).exists()

    def get_recipes(self, obj):
        """Метод для получения рецептов."""
        recipes = obj.following.recipe.all()
        return FollowRecipeSerializer(
            recipes,
            many=True).data

    def validate(self, data):
        """Функция валидации подписок."""
        user = self.context.get('request').user
        following = self.context.get('following_id')
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписаны на данного пользователя'})
        if user.id == int(following):
            raise serializers.ValidationError(
                'Невозможно подписаться на себя самого!')
        return data
