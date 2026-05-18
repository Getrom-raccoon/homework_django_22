from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Административный интерфейс для модели пользователя"""

    list_display = ('email', 'phone', 'country', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'country')
    search_fields = ('email', 'phone', 'country')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': ('phone', 'country', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'country', 'avatar', 'is_staff', 'is_active'),
        }),
    )

    ordering = ('email',)