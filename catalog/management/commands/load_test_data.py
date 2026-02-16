from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    """Кастомная команда для загрузки тестовых данных"""

    help = 'Загружает тестовые данные в базу данных'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Начинаю загрузку тестовых данных...'))

        self.stdout.write('Удаляю существующие данные...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Создаю категории...')
        categories_data = [
            {'name': 'Рассылки', 'description': 'Программы для автоматизации email-рассылок'},
            {'name': 'Телеграм боты', 'description': 'Готовые решения для Telegram ботов'},
            {'name': 'Полезные утилиты', 'description': 'Вспомогательные программы для разработчиков'},
            {'name': 'Веб-приложения', 'description': 'Готовые веб-приложения и шаблоны'},
            {'name': 'Микросервисы', 'description': 'Архитектурные решения на основе микросервисов'}
        ]

        created_categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            created_categories.append(category)
            self.stdout.write(f'  Создана категория: {category.name}')

        self.stdout.write('Создаю продукты...')
        products_data = [
            {'name': 'Удобный сервис рассылок', 'description': 'Продвинутая система для email-маркетинга с аналитикой',
             'price': 140.00, 'category': created_categories[0]},
            {'name': 'Telegram CRM Bot', 'description': 'Бот для управления клиентами через Telegram', 'price': 89.99,
             'category': created_categories[1]},
            {'name': 'API Tester Pro', 'description': 'Утилита для тестирования REST API', 'price': 49.99,
             'category': created_categories[2]},
            {'name': 'E-commerce Template', 'description': 'Готовый шаблон интернет-магазина на Django',
             'price': 199.99, 'category': created_categories[3]},
            {'name': 'Auth Microservice', 'description': 'Микросервис для аутентификации пользователей',
             'price': 299.99, 'category': created_categories[4]},
            {'name': 'Newsletter Automator', 'description': 'Автоматизация рассылки новостных писем', 'price': 120.00,
             'category': created_categories[0]}
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(f'  Создан продукт: {product.name} - {product.price} руб.')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
        self.stdout.write(f'Создано: {Category.objects.count()} категорий, {Product.objects.count()} продуктов')