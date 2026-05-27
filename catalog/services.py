from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция для получения всех продуктов в указанной категории
    с использованием низкоуровневого кеширования
    """
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        try:
            category = Category.objects.get(pk=category_id)
            products = Product.objects.filter(
                category=category,
                is_published=True
            ).select_related('category', 'owner')

            cache.set(cache_key, products, timeout=600)
            print(f'Продукты категории {category_id} загружены из БД и сохранены в кеш')
        except Category.DoesNotExist:
            products = []
            cache.set(cache_key, products, timeout=60)
            print(f'Категория {category_id} не найдена')
    else:
        print(f'Продукты категории {category_id} загружены из кеша Redis')

    return products