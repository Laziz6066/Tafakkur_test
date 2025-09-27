from django.test import TestCase
from catalog.models import Category, Product


class CategoryModelTest(TestCase):
    """
    TestCase для тестирования модели Category.

    Тестирует:
    - Создание категории с различными атрибутами
    - Строковое представление категории
    - Метод получения URL изображения

    Fixtures:
    - Создает тестовую категорию в setUp
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Создает экземпляр категории для использования в тестах.
        """
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )

    def test_category_creation(self):
        """
        Тестирование корректного создания категории.

        Проверяет:
        - Правильность сохранения имени категории
        - Правильность сохранения описания категории
        """
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test description")

    def test_category_str(self):
        """
        Тестирование строкового представления категории.

        Проверяет что __str__ возвращает название категории.
        """
        self.assertEqual(str(self.category), "Test Category")

    def test_category_get_image_url(self):
        """
        Тестирование метода получения URL изображения категории.

        Проверяет:
        - Метод возвращает строку
        - Для категории без изображения возвращается пустая строка
        """
        url = self.category.get_image_url()
        self.assertIsInstance(url, str)
        self.assertEqual(url, "")


class ProductModelTest(TestCase):
    """
    TestCase для тестирования модели Product.

    Тестирует:
    - Создание товара с связью с категорией
    - Строковое представление товара
    - Метод получения URL изображения товара

    Fixtures:
    - Создает тестовую категорию и товар в setUp
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Создает категорию и товар для использования в тестах.
        """
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=100.50,
            description="Test product description"
        )

    def test_product_creation(self):
        """
        Тестирование корректного создания товара.

        Проверяет:
        - Правильность сохранения названия товара
        - Корректность преобразования цены в float
        - Правильность связи с категорией
        - Правильность сохранения описания товара
        """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(float(self.product.price), 100.50)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.description, "Test product description")

    def test_product_str(self):
        """
        Тестирование строкового представления товара.

        Проверяет что __str__ возвращает название товара.
        """
        self.assertEqual(str(self.product), "Test Product")

    def test_product_get_image_url(self):
        """
        Тестирование метода получения URL изображения товара.

        Проверяет:
        - Метод возвращает строку
        - Для товара без изображения возвращается пустая строка
        """
        url = self.product.get_image_url()
        self.assertIsInstance(url, str)
        self.assertEqual(url, "")
