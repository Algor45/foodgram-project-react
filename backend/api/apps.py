"""Write your api app settings here."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Set your api app name here."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
