from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с авторизацией по email"""

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        help_text='Загрузите изображение профиля',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=35,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        help_text='Введите страну проживания',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email