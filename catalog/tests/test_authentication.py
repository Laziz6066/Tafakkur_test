from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class JWTAuthenticationTest(APITestCase):
    """
    Тестовый класс для проверки JWT аутентификации в Django REST Framework.

    Этот класс содержит тесты для проверки корректности работы JWT токенов:
    - получения access и refresh токенов
    - обновления access токена с помощью refresh токена
    - доступа к защищенным эндпоинтам с использованием JWT токена

    Наследуется от APITestCase для использования
    API-ориентированных методов тестирования.
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед выполнением каждого теста.

        Создает тестового пользователя и определяет URL-адреса для:
        - получения токенов (token_obtain_pair)
        - обновления токена (token_refresh)
        - защищенного эндпоинта (category-list) для проверки доступа
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.token_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.categories_url = reverse("category-list")

    def test_jwt_token_obtain(self):
        """
        Тестирование получения JWT токенов (access и refresh).

        Проверяет, что при корректных учетных данных пользователя:
        - возвращается статус 200 OK
        - в ответе присутствуют access и refresh токены
        - аутентификация через JWT работает корректно
        """
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_token_refresh(self):
        """
        Тестирование обновления access токена с помощью refresh токена.

        Процесс тестирования:
        1. Сначала получает пару токенов (access и refresh)
        2. Использует refresh токен для получения нового access токена
        3. Проверяет, что операция обновления проходит успешно
        4. Убеждается, что возвращается новый access токен
        """
        # First get tokens
        token_response = self.client.post(self.token_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        refresh_token = token_response.data["refresh"]

        # Refresh access token
        refresh_response = self.client.post(self.refresh_url,
                                            {"refresh": refresh_token})
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

    def test_protected_endpoint_with_token(self):
        """
        Тестирование доступа к защищенному эндпоинту
        с использованием JWT токена.

        Проверяет, что:
        1. Полученный access токен предоставляет доступ
        к защищенным ресурсам
        2. Запрос к защищенному эндпоинту не возвращает
        статус 401 (Unauthorized)
        3. JWT аутентификация корректно интегрирована с
        защищенными эндпоинтами
        """
        # Get token
        token_response = self.client.post(self.token_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        access_token = token_response.data["access"]

        # Access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.categories_url,
                                    {"name": "New Category"})
        self.assertNotEqual(response.status_code,
                            status.HTTP_401_UNAUTHORIZED)
