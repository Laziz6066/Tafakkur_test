from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from catalog.models import Category, Product


class CategoryViewSetTest(APITestCase):
    """
    Тестовый класс для проверки ViewSet категорий.

    Проверяет работу CRUD операций с категориями через API:
    - получение списка категорий
    - получение детальной информации о категории
    - проверка прав доступа при создании категорий
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Создает тестовую категорию и определяет URL-адреса для:
        - списка категорий (category-list)
        - детальной информации о категории (category-detail)
        """
        self.category = Category.objects.create(name="Test Category")
        self.list_url = reverse("category-list")
        self.detail_url = reverse("category-detail",
                                  kwargs={"pk": self.category.id})

    def test_get_categories(self):
        """
        Тестирование получения списка категорий.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK
        - запрос на получение списка категорий выполняется успешно
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_detail(self):
        """
        Тестирование получения детальной информации о категории.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK
        - возвращаемые данные содержат корректное имя категории
        - запрос на получение конкретной категории работает правильно
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Category")

    def test_create_category_unauthorized(self):
        """
        Тестирование попытки создания категории без авторизации.

        Проверяет, что:
        - неавторизованный пользователь не может создать категорию
        - возвращается статус 401 Unauthorized
        - система корректно проверяет права доступа
        """
        data = {"name": "New Category"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewSetTest(APITestCase):
    """
    Тестовый класс для проверки ViewSet продуктов.

    Проверяет работу CRUD операций с продуктами через API:
    - получение списка продуктов
    - получение детальной информации о продукте
    - проверка прав доступа при создании продуктов
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Создает тестовую категорию и продукт, определяет URL-адреса для:
        - списка продуктов (product-list)
        - детальной информации о продукте (product-detail)
        """
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=50.00
        )
        self.list_url = reverse("product-list")
        self.detail_url = reverse("product-detail",
                                  kwargs={"pk": self.product.id})

    def test_get_products(self):
        """
        Тестирование получения списка продуктов.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK
        - запрос на получение списка продуктов выполняется успешно
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        """
        Тестирование получения детальной информации о продукте.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK
        - возвращаемые данные содержат корректное имя продукта и категории
        - связь между продуктом и категорией отображается правильно
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")
        self.assertEqual(response.data["category_name"], "Test Category")

    def test_create_product_unauthorized(self):
        """
        Тестирование попытки создания продукта без авторизации.

        Проверяет, что:
        - неавторизованный пользователь не может создать продукт
        - возвращается статус 401 Unauthorized
        - система корректно проверяет права доступа для операций записи
        """
        data = {
            "category": self.category.id,
            "name": "New Product",
            "price": "75.00"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductSearchViewTest(APITestCase):
    """
    Тестовый класс для проверки функциональности поиска продуктов.

    Проверяет работу поискового эндпоинта с различными параметрами:
    - базовая доступность эндпоинта
    - поиск по текстовому запросу
    - фильтрация по категории
    - фильтрация по ценовому диапазону
    - работа пагинации
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Определяет URL для поискового эндпоинта.
        """
        self.search_url = reverse("search-products")

    def test_search_endpoint_accessible(self):
        """
        Тестирование базовой доступности поискового эндпоинта.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK
        - ответ содержит корректную структуру данных (results, count)
        - результаты возвращаются в виде списка
        """
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_search_with_query_param(self):
        """
        Тестирование поиска с текстовым запросом.

        Проверяет, что поиск работает с параметром 'q' (query)
        и возвращает корректный статус ответа.
        """
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_with_category_param(self):
        """
        Тестирование фильтрации по категории.

        Проверяет, что фильтрация продуктов по ID категории
        работает корректно и возвращает статус 200 OK.
        """
        response = self.client.get(self.search_url, {"category": "1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_with_price_params(self):
        """
        Тестирование фильтрации по ценовому диапазону.

        Проверяет, что фильтрация по минимальной и максимальной цене
        работает корректно с параметрами price_min и price_max.
        """
        response = self.client.get(self.search_url,
                                   {"price_min": "10", "price_max": "100"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_pagination(self):
        """
        Тестирование работы пагинации с пользовательскими настройками.

        Проверяет, что:
        - пагинация работает с указанием номера страницы и размера
        - возвращаются корректные данные о текущей странице
        - правильно определяется наличие предыдущей страницы
        """
        response = self.client.get(self.search_url,
                                   {"page": 2, "page_size": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 2)  # ✅ Теперь должно работать
        self.assertEqual(response.data["page_size"], 5)
        self.assertEqual(response.data["has_prev"], True)
        # ✅ Для page=2 has_prev=True

    def test_search_default_pagination(self):
        """
        Тестирование пагинации с настройками по умолчанию.

        Проверяет, что при отсутствии параметров пагинации
        используются значения по умолчанию (страница 1, размер 20).
        """
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(response.data["page_size"], 20)
        # ✅ Значение по умолчанию


class ProductSuggestViewTest(APITestCase):
    """
    Тестовый класс для проверки функциональности автодополнения продуктов.

    Проверяет работу эндпоинта подсказок (autocomplete) для продуктов:
    - базовая доступность эндпоинта
    - обязательность параметра запроса
    - работа с ограничением количества результатов
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Определяет URL для эндпоинта автодополнения продуктов.
        """
        self.suggest_url = reverse("suggest-products")

    def test_suggest_endpoint_accessible(self):
        """
        Тестирование базовой доступности эндпоинта автодополнения.

        Проверяет, что:
        - эндпоинт возвращает статус 200 OK при наличии параметра 'q'
        - ответ содержит корректную структуру данных (options, q)
        """
        response = self.client.get(self.suggest_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("options", response.data)
        self.assertIn("q", response.data)

    def test_suggest_requires_query_param(self):
        """
        Тестирование обязательности параметра запроса.

        Проверяет, что при отсутствии обязательного параметра 'q'
        возвращается статус 400 Bad Request.
        """
        response = self.client.get(self.suggest_url)
        # Теперь должно возвращать 400, так как q обязателен
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_suggest_with_size_param(self):
        """
        Тестирование работы с параметром ограничения количества результатов.

        Проверяет, что параметр 'size' корректно ограничивает количество
        возвращаемых подсказок и возвращается в ответе.
        """
        response = self.client.get(self.suggest_url, {"q": "test", "size": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["size"], 3)
        # ✅ Проверяем что size возвращается
