from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """Модель категории продуктов"""

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование категории',
        help_text='Введите наименование категории'
    )

    description = models.TextField(
        verbose_name='Описание категории',
        help_text='Введите описание категории',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование продукта',
        help_text='Введите наименование продукта'
    )

    description = models.TextField(
        verbose_name='Описание продукта',
        help_text='Введите описание продукта',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение продукта',
        help_text='Загрузите изображение продукта',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория продукта',
        help_text='Выберите категорию продукта',
        null=True,
        blank=True,
        related_name='products'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена продукта',
        help_text='Введите цену продукта'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Владелец',
        help_text='Пользователь, создавший продукт',
        null=True,
        blank=True,
        related_name='products'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отметьте, чтобы опубликовать продукт'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'category']

        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_delete_any_product', 'Может удалять любой продукт'),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'category']

    def __str__(self):
        return f"{self.name} - {self.price} руб."