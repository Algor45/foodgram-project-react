"""Write your recipes app settings here."""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Set your recipes app name here."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
