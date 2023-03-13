"""Write your api app pagination here."""
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация."""

    page_size = 6
    page_size_query_param = 'limit'
