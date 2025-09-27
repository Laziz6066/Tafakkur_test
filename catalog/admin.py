from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административный класс для управления категориями в Django Admin.

    Настраивает отображение и функциональность модели Category в админ-панели:
    - определяет какие поля отображать в списке объектов
    - обеспечивает удобный интерфейс для управления категориями
    """
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административный класс для управления продуктами в Django Admin.

    Настраивает расширенное отображение и функциональность модели Product:
    - определяет поля для отображения в списке продуктов
    - добавляет фильтрацию по категориям для удобной навигации
    - реализует поиск по названию и описанию продуктов
    """
    list_display = ("id", "name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "description")
