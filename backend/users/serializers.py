"""Write your api app serializers here."""
from rest_framework import serializers
from recipes.models import Recipe
from users.models import CustomUser, Follow
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(UserSerializer):
    """Сериалайзер для модели CustomUser."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Meta настройки сериалайзера для модели CustomUser."""

        model = CustomUser
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        """Метод для получения свойства is_subscribed."""
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Follow.objects.filter(user=request.user,
                                         following=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для регистрации нового пользователя."""

    class Meta:
        """Meta настройки сериалайзера для модели создания пользователя."""

        model = CustomUser
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password'
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для кратких рецептов в подписках."""

    image = Base64ImageField()

    class Meta:
        """Meta настройки сериалайзера кратких рецептов."""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Follow."""

    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
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
            user=obj.user,
            following=obj.following
        ).exists()

    def get_recipes(self, obj):
        """Метод для получения рецептов."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.following)
        if limit:
            queryset = queryset[:int(limit)]
        return FollowRecipeSerializer(queryset, many=True).data

    def validate(self, data):
        """Функция валидации невозможности подписаться на себя."""
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя самого!')
        return data
