"""Set your Posts models here."""
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(verbose_name='Тэг',
                            help_text='Укажите Тэг',
                            unique=True,
                            max_length=20)
    color = models.CharField(verbose_name='Цвет',
                             unique=True,
                             default='#00ff7f',
                             help_text='Укажите цвет в формате HEX',
                             max_length=7)
    slug = models.SlugField(verbose_name='Ссылка',
                            help_text='Укажите уникальную ссылку',
                            unique=True)

    class Meta:
        """Мета настройки модели Tag."""

        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        """Функция __str__ модели Tag."""
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(verbose_name='Название ингредиента',
                            help_text='Укажите название ингредиента',
                            max_length=100,
                            blank=False,
                            null=False)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        help_text='Укажите ед.изм.',
                                        max_length=50)

    class Meta:
        """Meta модели Ingredient."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)

    def __str__(self) -> str:
        """Функция __str__ модели Ingredient."""
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    name: str = models.CharField(verbose_name='Название рецепта',
                                 help_text='Укажите название рецепта',
                                 max_length=100)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    image = models.ImageField('Картинка',
                              upload_to='recipes')
    text = models.TextField(verbose_name='Описание рецепта',
                            help_text='Опишите рецепт')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='тэг',
                                  related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Укажите время приготовления (в минутах)')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    help_text='Укажите дату')

    class Meta:
        """Meta модели Recipe."""

        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        """Функция __str__ модели Recipe."""
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи моделей Recipe Ingredient."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient')
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=(MinValueValidator(
                    1, message='Минимальное количество ингредиентов 1'),)
    )

    class Meta:
        """Meta модели RecipeIngredient."""

        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'],
            name='unique_ingredient')
        ]

        def __str__(self):
            """Функция __str__ модели RecipeIngredient."""
            return (f'Ингредиент {self.ingredient.name}'
                    f' содержится в рецепте {self.reipe.name}')


class Cart(models.Model):
    """Модель Cart."""

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='cart')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='cart_recipe')

    class Meta:
        """Meta модели Cart."""

        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_cart')]

    def __str__(self) -> str:
        """Функция __str__ модели Cart."""
        return (f'{self.recipe.name} в корзине'
                f'у пользователя {self.user.username}')


class Favorite(models.Model):
    """Модель Favorite."""

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='favorite')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='favorite_recipe')

    class Meta:
        """Meta модели Favorite."""

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_favorite')]

    def __str__(self) -> str:
        """Функция __str__ модели Cart."""
        return (f'{self.recipe.name} в избранном'
                f'у пользователя {self.user.username}')
