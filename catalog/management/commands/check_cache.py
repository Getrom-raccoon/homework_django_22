from django.core.management.base import BaseCommand
from django.core.cache import cache
from catalog.models import Product, Category
from catalog.services import get_products_by_category


class Command(BaseCommand):
    """Команда для проверки работы кеширования"""

    help = 'Проверяет работу кеширования Redis'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Проверка кеширования...'))

        test_key = 'test_cache'
        cache.set(test_key, 'Redis работает!', timeout=60)
        result = cache.get(test_key)

        if result:
            self.stdout.write(self.style.SUCCESS(f'Кеш Redis работает: {result}'))
        else:
            self.stdout.write(self.style.ERROR('Кеш Redis не работает'))

        products = Product.objects.filter(is_published=True)[:5]
        for product in products:
            cache_key = f'product_{product.pk}'
            cached = cache.get(cache_key)
            self.stdout.write(f'Продукт {product.pk}: {"в кеше" if cached else "не в кеше"}')

        categories = Category.objects.all()
        for category in categories:
            products_list = get_products_by_category(category.pk)
            self.stdout.write(f'Категория {category.name}: {len(products_list) if products_list else 0} товаров')

        self.stdout.write(self.style.SUCCESS('Проверка завершена'))