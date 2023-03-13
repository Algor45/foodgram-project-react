"""Migration."""
# Generated by Django 3.2.18 on 2023-03-09 00:08

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Укажите цвет в формате #FFFFFF', max_length=7, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Укажите Тэг', max_length=20, unique=True, verbose_name='Тэг'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальную ссылку', unique=True, verbose_name='Ссылка'),
        ),
    ]
