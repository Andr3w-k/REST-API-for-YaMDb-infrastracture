"""reviews."""
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


def current_year():
    """current_year."""
    return datetime.date.today().year


def max_value_current_year(value):
    """max_value_current_year."""
    return MaxValueValidator(
        current_year(),
        'Год релиза должен быть не позднее текущего года'
    )(value)


class Category(models.Model):
    """Category."""
    name = models.CharField(
        'Название',
        max_length=200
    )
    slug = models.SlugField(
        'Код категории(eng)',
        unique=True
    )

    def __str__(self):
        """Category_sttr."""
        return self.name


class Genres(models.Model):
    """Genres."""
    name = models.CharField(
        'Название жанра',
        max_length=50
    )
    slug = models.SlugField(
        'Slug жанра',
        unique=True
    )

    def __str__(self):
        """Genres_str."""
        return self.name


class Title(models.Model):
    """Title."""
    name = models.CharField(
        'Название',
        max_length=250
    )
    year = models.PositiveSmallIntegerField(
        'Год релиза',
        db_index=True,
        default=current_year(),
        validators=[
            MinValueValidator(1895, 'Год релиза должен быть не ранее 1895'),
            max_value_current_year],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='genres'
    )
    description = models.TextField(
        'Описание',
        blank=True
    )

    def __str__(self):
        """Title_str."""
        return self.name


class Review(models.Model):
    """Review."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        'Содержание',
        max_length=500,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        default=5,
        validators=[
            MinValueValidator(
                1,
                'Оценка должна быть числом в пределах от 1 до 10'
            ),
            MaxValueValidator(
                10,
                'Оценка должна быть числом в пределах от 1 до 10'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        """Review_Meta."""
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review'),
        )

    STR_METOD_TEMPLATE = (
        'Обзор: {text:.15}... '
        'Дата публикации: {date:%d %b %Y}. '
        'Автор: {author}. '
        'К произведению: {title}. '
        'Оценка: {score}'
    )

    def __str__(self):
        """Review_str."""
        return self.STR_METOD_TEMPLATE.format(
            text=self.text,
            date=self.pub_date,
            author=self.author.username,
            title=self.title,
            score=self.score
        )


class Comment(models.Model):
    """Comment."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        'Содержание',
        max_length=500,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        """Comment_Meta."""
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Comment_str."""
        return self.text[:15]
