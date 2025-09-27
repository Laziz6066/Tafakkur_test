import sys

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product


@registry.register_document
class ProductDocument(Document):
    """
    Elasticsearch документ для модели Product.

    Определяет схему индексации продуктов в Elasticsearch
    для полнотекстового поиска.
    Включает основные поля продукта, связанные данные
    категории и поле для автодополнения.
    """
    category = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
    })

    category_id = fields.IntegerField(attr="category.id")
    image = fields.TextField(attr="image.url")
    price = fields.FloatField()
    suggest = fields.CompletionField()  # Поле для автодополнения и предложений

    class Index:
        """
        Конфигурация индекса Elasticsearch.

        Определяет настройки индекса для хранения продуктов:
        - name: название индекса в Elasticsearch
        - settings: конфигурация шардов и реплик для оптимизации
         производительности
        """
        name = "products"
        settings = {
            'number_of_shards': 1,  # Количество шардов
            # для распределения данных
            'number_of_replicas': 0  # Количество реплик
            # для отказоустойчивости
        }

    class Django:
        """
        Связь с Django моделью и настройка полей для индексации.

        Определяет:
        - model: Django модель, связанная с документом
        - fields: список полей модели, которые будут
        индексироваться в Elasticsearch
        """
        model = Product
        fields = [
            "id",
            "name",
            "description",
        ]

    def get_queryset(self):
        """
        Оптимизация запроса к базе данных для индексации.

        Использует select_related для предварительной загрузки
        связанных данных категории,
        что уменьшает количество SQL-запросов при индексации продуктов.
        """
        return super().get_queryset().select_related('category')

    def update(self, thing, refresh=None, action='index',
               parallel=False, **kwargs):
        """
        Переопределение метода обновления для исключения
        операций в тестовом режиме.

        Пропускает обновление индекса Elasticsearch при запуске тестов,
        чтобы избежать побочных эффектов и ускорить выполнение тестов.
        """
        if 'test' in sys.argv:
            return None  # Пропускаем в тестах
        return super().update(thing, refresh, action, parallel, **kwargs)

    def delete(self, refresh=None, **kwargs):
        """
        Переопределение метода удаления для исключения
         операций в тестовом режиме.

        Пропускает удаление из индекса Elasticsearch при запуске тестов,
        чтобы тесты не влияли на поисковый индекс.
        """
        if 'test' in sys.argv:
            return None  # Пропускаем в тестах
        return super().delete(refresh, **kwargs)
