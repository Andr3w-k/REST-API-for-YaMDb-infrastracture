"""users_models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User."""
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    password = models.CharField(
        max_length=128,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    email = models.EmailField(
        'Email адрес',
        unique=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False
    )
    role = models.CharField(
        'Уровень доступа',
        max_length=16,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """User_str."""
        return self.username

    @property
    def is_user(self):
        """is_user."""
        return self.role == 'user'

    @property
    def is_moderator(self):
        """is_moderator."""
        return self.role == 'moderator'

    @property
    def is_admin(self):
        """is_admin."""
        return self.role == 'admin' or self.is_staff
