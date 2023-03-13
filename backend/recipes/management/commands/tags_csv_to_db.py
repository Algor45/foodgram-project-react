"""Write your csv_to_db import here."""
import csv
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """Класс Command для имопрта tags из csv в db."""

    help = 'Tag from csv load'

    def handle(self, *args, **options):
        """Метод импортирующий данные tags."""
        with open('data/tags.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                created = Tag.objects.get_or_create(
                        name=row[0],
                        color=row[1],
                        slug=row[2]
                        )
