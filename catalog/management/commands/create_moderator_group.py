from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    """Кастомная команда для создания группы модераторов"""

    help = 'Создает группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Создаю группу модераторов...'))

        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish, created1 = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type,
            defaults={'name': 'Может отменять публикацию продукта'}
        )

        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        if created1:
            self.stdout.write('Создано разрешение can_unpublish_product')

        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        moderator_group.permissions.add(can_unpublish, can_delete)
        self.stdout.write('Права назначены группе')

        self.stdout.write(self.style.SUCCESS('Готово!'))
        self.stdout.write(f'Группа: {moderator_group.name}')
        self.stdout.write(f'Права: {list(moderator_group.permissions.values_list("codename", flat=True))}')