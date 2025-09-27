from django.core.management.base import BaseCommand
from catalog.documents import ProductDocument
from catalog.models import Product


class Command(BaseCommand):
    """
    Management command для индексации товаров в Elasticsearch.

    Команда выполняет полную переиндексацию всех товаров в Elasticsearch:
    - Удаляет существующий индекс (если существует)
    - Создает новый индекс с актуальной схемой
    - Индексирует все товары из базы данных

    Использование:
        python manage.py populate_es

    Применение:
    - Первоначальная настройка поиска после развертывания
    - Восстановление индекса после изменений в mapping
    - Обновление индекса после массовых изменений товаров

    Особенности:
    - Использует select_related для оптимизации запросов к БД
    - Обрабатывает связанные данные категорий
    - Игнорирует ошибки при удалении несуществующего индекса
    """

    help = 'Index all products in Elasticsearch'

    def handle(self, *args, **options):
        """
        Основной метод выполнения команды.

        Выполняет последовательность операций:
        1. Удаление старого индекса (если существует)
        2. Создание нового индекса с актуальной схемой
        3. Индексация всех товаров из базы данных
        4. Вывод отчета о выполнении

        Args:
            *args: Дополнительные аргументы
            **options: Опции команды

        Returns:
            None

        Raises:
            ElasticsearchException: При ошибках взаимодействия с Elasticsearch
            DatabaseError: При ошибках доступа к базе данных

        Example:
            $ python manage.py populate_es
            Successfully indexed 150 products
        """

        # Удаление существующего индекса
        self.stdout.write("Deleting existing Elasticsearch index...")
        ProductDocument._index.delete(ignore=404)
        self.stdout.write(self.style.SUCCESS("Index deleted successfully"))

        # Создание нового индекса с актуальной схемой
        self.stdout.write("Creating new Elasticsearch index...")
        ProductDocument._index.create()
        self.stdout.write(self.style.SUCCESS("Index created successfully"))

        # Получение всех товаров с оптимизацией запроса
        self.stdout.write("Fetching products from database...")
        products = Product.objects.select_related('category').all()
        self.stdout.write(f"Found {products.count()} products to index")

        # Индексация каждого товара
        self.stdout.write("Indexing products in Elasticsearch...")
        indexed_count = 0

        for product in products:
            try:
                ProductDocument().update(product)
                indexed_count += 1

                # Вывод прогресса для больших наборов данных
                if indexed_count % 100 == 0:
                    self.stdout.write(f"Indexed {indexed_count} products...")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error indexing product "
                                     f"{product.id}: {str(e)}")
                )

        # Вывод итогового отчета
        self.stdout.write(
            self.style.SUCCESS(f"Successfully indexed "
                               f"{indexed_count} products")
        )

        # Дополнительная информация
        if indexed_count < products.count():
            self.stdout.write(
                self.style.WARNING(
                    f"Note: {products.count() - indexed_count}"
                    f" products failed to index"
                )
            )
