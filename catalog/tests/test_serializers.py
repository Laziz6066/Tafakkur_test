from django.test import TestCase

from catalog.models import Category, Product
from catalog.serializers import (CategorySerializer, ProductSerializer,
                                 SearchQuerySerializer, SuggestQuerySerializer)


class CategorySerializerTest(TestCase):
    """
    TestCase для тестирования CategorySerializer.

    Тестирует:
    - Сериализацию существующей категории
    - Создание новой категории через сериализатор
    - Валидацию данных категории
    """

    def setUp(self):
        """Подготовка тестовых данных."""
        self.category_data = {
            "name": "Serialized Category",
            "description": "Serialized description"
        }
        self.category = Category.objects.create(**self.category_data)

    def test_category_serializer(self):
        """
        Тестирование сериализации существующей категории.

        Проверяет корректность преобразования модели в JSON.
        """
        serializer = CategorySerializer(instance=self.category)
        self.assertEqual(serializer.data["name"], self.category_data["name"])
        self.assertEqual(serializer.data["description"],
                         self.category_data["description"])
        self.assertEqual(serializer.data["id"], self.category.id)

    def test_category_serializer_create(self):
        """
        Тестирование создания категории через сериализатор.

        Проверяет:
        - Валидность данных
        - Корректное создание объекта в базе данных
        """
        new_category_data = {
            "name": "New Category for Creation",
            "description": "New description"
        }
        serializer = CategorySerializer(data=new_category_data)
        self.assertTrue(serializer.is_valid(),
                        f"Serializer errors: {serializer.errors}")
        category = serializer.save()
        self.assertEqual(category.name, new_category_data["name"])

    def test_category_serializer_validation(self):
        """
        Тестирование валидации CategorySerializer.

        Проверяет обработку невалидных данных (отсутствие обязательного поля).
        """
        invalid_data = {
            "description": "Missing name field"
        }
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class ProductSerializerTest(TestCase):
    """
    TestCase для тестирования ProductSerializer.

    Тестирует:
    - Сериализацию существующего товара
    - Создание нового товара через сериализатор
    - Валидацию данных товара
    """

    def setUp(self):
        """Подготовка тестовых данных."""
        self.category = Category.objects.create(name="Test Category")
        self.product_data = {
            "category": self.category.id,
            "name": "Test Product",
            "price": "99.99",
            "description": "Test description"
        }

    def test_product_serializer(self):
        """
        Тестирование сериализации существующего товара.

        Проверяет включение дополнительного поля category_name.
        """
        product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=99.99
        )
        serializer = ProductSerializer(instance=product)
        self.assertEqual(serializer.data["name"], "Test Product")
        self.assertEqual(serializer.data["category_name"], "Test Category")
        self.assertEqual(serializer.data["category"], self.category.id)

    def test_product_serializer_create(self):
        """
        Тестирование создания товара через сериализатор.

        Проверяет корректное создание товара с связью с категорией.
        """
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(),
                        f"Serializer errors: {serializer.errors}")
        product = serializer.save()
        self.assertEqual(product.name, "Test Product")

    def test_product_serializer_validation(self):
        """
        Тестирование валидации ProductSerializer.

        Проверяет обработку невалидных данных (отсутствие обязательных полей).
        """
        invalid_data = {
            "name": "Missing category and price"
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
        self.assertIn("price", serializer.errors)


class SearchQuerySerializerTest(TestCase):
    """
    TestCase для тестирования SearchQuerySerializer.

    Тестирует валидацию параметров поискового запроса.
    """

    def test_valid_search_query(self):
        """Тестирование валидного поискового запроса со всеми параметрами."""
        data = {
            "q": "test product",
            "category": "1,2,3",
            "price_min": "10.00",
            "price_max": "100.00",
            "sort": "price_asc",
            "page": 1,
            "page_size": 10
        }
        serializer = SearchQuerySerializer(data=data)
        self.assertTrue(serializer.is_valid(),
                        f"Serializer errors: {serializer.errors}")
        self.assertEqual(serializer.validated_data["category"], [1, 2, 3])

    def test_empty_search_query(self):
        """Тестирование пустого поискового запроса."""
        data = {}
        serializer = SearchQuerySerializer(data=data)
        self.assertTrue(serializer.is_valid(),
                        f"Serializer errors: {serializer.errors}")

    def test_invalid_category_format(self):
        """Тестирование невалидного формата категорий."""
        data = {"category": "1,abc,3"}
        serializer = SearchQuerySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

    def test_price_validation(self):
        """Тестирование валидации диапазона цен."""
        data = {"price_min": "100.00", "price_max": "50.00"}
        serializer = SearchQuerySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class SuggestQuerySerializerTest(TestCase):
    """
    TestCase для тестирования SuggestQuerySerializer.

    Тестирует валидацию параметров запроса подсказок.
    """

    def test_valid_suggest_query(self):
        """Тестирование валидного запроса подсказок."""
        data = {"q": "test", "size": 5}
        serializer = SuggestQuerySerializer(data=data)
        self.assertTrue(serializer.is_valid(),
                        f"Serializer errors: {serializer.errors}")

    def test_missing_query(self):
        """Тестирование запроса без обязательного параметра q."""
        data = {"size": 5}
        serializer = SuggestQuerySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("q", serializer.errors)

    def test_empty_query(self):
        """Тестирование запроса с пустым параметром q."""
        data = {"q": ""}
        serializer = SuggestQuerySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("q", serializer.errors)

    def test_size_validation(self):
        """Тестирование валидации параметра size."""
        data = {"q": "test", "size": 20}  # больше максимума
        serializer = SuggestQuerySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("size", serializer.errors)
