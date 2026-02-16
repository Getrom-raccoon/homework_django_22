from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Category"""

    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('name',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Product"""

    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name', 'price')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('wide',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')