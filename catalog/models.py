from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
import sys


class Category(models.Model):
    """
    Модель категории товаров.

    Attributes:
        name (str): Название категории (уникальное)
        description (str): Описание категории
        image (ImageField): Изображение категории
    """

    name = models.CharField("название", max_length=255, unique=True)
    description = models.TextField("описание", blank=True)
    image = models.ImageField("изображение",
                              upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Строковое представление категории."""
        return self.name

    def get_image_url(self):
        """
        Получить URL изображения категории.

        Returns:
            str: URL изображения или пустая строка если изображение отсутствует
        """
        return self.image.url if self.image else ""


class Product(models.Model):
    """
    Модель товара.

    Attributes:
        category (Category): Связь с категорией
        name (str): Название товара
        price (Decimal): Цена товара
        image (ImageField): Изображение товара
        description (str): Описание товара
    """

    category = models.ForeignKey(Category, related_name="products",
                                 on_delete=models.CASCADE)
    name = models.CharField("название", max_length=255)
    price = models.DecimalField("цена", max_digits=12, decimal_places=2)
    image = models.ImageField("изображение",
                              upload_to="products/", blank=True, null=True)
    description = models.TextField("описание", blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        """Строковое представление товара."""
        return self.name

    def get_image_url(self):
        """
        Получить URL изображения товара.

        Returns:
            str: URL изображения или пустая строка если изображение отсутствует
        """
        return self.image.url if self.image else ""


# Сигналы для Elasticsearch (только в не-тестовом режиме)
if 'test' not in sys.argv:
    @receiver(post_save, sender=Product)
    def index_product(sender, instance, **kwargs):
        """
        Сигнал для индексации товара в Elasticsearch после сохранения.

        Args:
            sender: Модель, отправившая сигнал
            instance: Экземпляр модели Product
            **kwargs: Дополнительные аргументы
        """
        registry.update(instance)
        registry.update_related(instance)

    @receiver(post_delete, sender=Product)
    def delete_product(sender, instance, **kwargs):
        """
        Сигнал для удаления товара из Elasticsearch после удаления.

        Args:
            sender: Модель, отправившая сигнал
            instance: Экземпляр модели Product
            **kwargs: Дополнительные аргументы
        """
        registry.delete(instance, raise_on_error=False)

    @receiver(post_save, sender=Category)
    def update_products_on_category_change(sender, instance, **kwargs):
        """
        Сигнал для обновления связанных товаров при изменении категории.

        Args:
            sender: Модель, отправившая сигнал
            instance: Экземпляр модели Category
            **kwargs: Дополнительные аргументы
        """
        for product in instance.products.all():
            registry.update(product)
