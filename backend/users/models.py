"""Set your Posts models here."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Логин'
    )
    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='Электронный адрес'
    )
    first_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Фамилия'
    )
    password = models.CharField(max_length=150,
                                verbose_name='Пароль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        """Meta модели CustomUser."""

        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Функция __str__ модели CustomUser."""
        return self.username


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Следят',
    )

    class Meta:
        """Meta модели Follow."""

        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_user_following')]
