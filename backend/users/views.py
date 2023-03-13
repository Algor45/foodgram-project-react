"""Write your users app view functions here."""
from .models import CustomUser, Follow
from djoser.views import UserViewSet
from .serializers import FollowSerializer
from api.pagintaion import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.permissions import (IsAuthenticated)


class UserViewSet(UserViewSet):
    """Viewset для модели CustomUser и UserSerializer."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['POST', 'DELETE']
    )
    def subscribe(self, request, pk=None):
        """Метод для подписки и отписки."""
        user = request.user
        following = get_object_or_404(CustomUser, id=pk)
        if self.request.method == 'POST':
            if Follow.objects.filter(user=user, following=following).exists():
                return Response(
                    {'errors': 'Подписка уже существует.'},
                    status=HTTP_400_BAD_REQUEST
                )
            if user == following:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя.'},
                    status=HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.create(user=user, following=following)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if Follow.objects.filter(user=user, following=following).exists():
            follow = get_object_or_404(Follow, user=user, following=following)
            follow.delete()
            return Response(
                'Вы успешно отписались.',
                status=HTTP_204_NO_CONTENT
            )
        if user == following:
            return Response(
                {'errors': 'Невозможно отписаться от себя.'},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {'errors': 'Подписка отсутствует.'},
            status=HTTP_400_BAD_REQUEST
        )

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
