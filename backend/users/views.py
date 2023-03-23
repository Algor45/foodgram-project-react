"""Set your users Views here."""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import (IsAuthenticated,)
from .serializers import (UserSerializer, UserCreateSerializer,
                          FollowSerializer, SetPasswordSerializer)
from .models import Follow
from rest_framework.status import (HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

User = get_user_model()


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Mixin CreateDestroy."""
    pass


class UserViewSet(UserViewSet):
    """Viewset для модели CustomUser и UserSerializer."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """Выбор сериалайзера в зависимости от запроса."""
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """Разрешение на обращение к эндпоинту /me/."""
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET']
    )
    def subscriptions(self, request):
        """Метод для получения списка подписчиков."""
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FollowViewSet(CreateDestroyViewSet):
    """ViewSet для создания и удаления подписок."""

    serializer_class = FollowSerializer

    def get_queryset(self):
        """Переопределение метода get_queryset."""
        return self.request.user.follower.all()

    def get_serializer_context(self):
        """Переопределение метода get_serializer_context."""
        context = super().get_serializer_context()
        context['following_id'] = self.kwargs.get('user_id')
        return context

    def perform_create(self, serializer):
        """Переопределение метода preform_create."""
        serializer.save(
            user=self.request.user,
            following=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, user_id):
        """Метод удаления подписки."""
        get_object_or_404(User, id=user_id)
        if not Follow.objects.filter(
                user=request.user, following_id=user_id).exists():
            return Response({'errors': 'Вы не были подписаны на автора'},
                            status=HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Follow,
            user=request.user,
            following_id=user_id
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
