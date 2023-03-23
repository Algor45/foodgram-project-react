"""Write your csv_to_db import here."""
import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Класс Command для имопрта ingredients из csv в db."""

    help = 'ingredient from csv load'

    def handle(self, *args, **options):
        """Метод импортирующий данные ingredients."""
        with open('data/ingredients.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1])
