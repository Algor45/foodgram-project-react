"""Write here Admin settings for users app."""
from django.contrib import admin
from users.models import Follow, CustomUser


class UserAdmin(admin.ModelAdmin):
    """Настройки администратора для модели CustomUser."""

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email', 'last_name')
    list_filter = ('username', 'email', 'first_name', 'last_name')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    """Настройки администратора для модели Follow."""

    list_display = (
        'pk',
        'user',
        'following'
    )
    list_filter = ('user', 'following')
    search_fields = ('user__username', 'user__email')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Follow, FollowAdmin)
