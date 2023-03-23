"""Write here Admin settings for users app."""
from django.contrib import admin
from users.models import User, Follow


class UserAdmin(admin.ModelAdmin):
    """Настройки администратора для модели User."""

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email', 'last_name')
    list_filter = ('username', 'email', 'first_name')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Follow."""

    list_display = (
        'id',
        'user',
        'following'
    )
    list_filter = ('user', 'following')
    search_fields = ('user', 'following')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
