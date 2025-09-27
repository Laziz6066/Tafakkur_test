# 🛒 Shop API (DRF + PostgreSQL + JWT + Elasticsearch)

Этот проект — учебное Django-приложение с REST API для управления продуктами и категориями.  
Основные технологии:
- **Django REST Framework (DRF)** — API и CRUD
- **PostgreSQL** — основная база данных
- **JWT (SimpleJWT)** — авторизация
- **Elasticsearch + django-elasticsearch-dsl** — полнотекстовый поиск по продуктам
- **Docker Compose** — запуск всей инфраструктуры (Django + Postgres + Elasticsearch + Kibana)

---

## 📂 Структура проекта

```
Tafakkur_test/
├── catalog/ # Основное приложение
│ ├── management/
│ │ └── commands/ # Кастомные management команды
│ │ ├── populate_es.py # Индексация данных в Elasticsearch
│ │ └── wait_for_db.py # Ожидание готовности БД
│ ├── migrations/ # Миграции базы данных
│ ├── tests/ # Тесты приложения
│ │ ├── mocks.py # Mock-объекты для тестов
│ │ ├── test_authentication.py # Тесты аутентификации
│ │ ├── test_models.py # Тесты моделей
│ │ ├── test_serializers.py # Тесты сериализаторов
│ │ └── test_views.py # Тесты представлений
│ ├── init.py
│ ├── admin.py # Настройки Django Admin
│ ├── apps.py # Конфигурация приложения
│ ├── documents.py # Elasticsearch документы
│ ├── models.py # Модели данных (Category, Product)
│ ├── serializers.py # DRF сериализаторы
│ ├── urls.py # URL-маршруты приложения
│ └── views.py # Представления (ViewSets, APIView)
├── shop/ # Настройки проекта
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py # Основные настройки
│ ├── urls.py # Корневые URL
│ └── wsgi.py
├── media/ # Загружаемые файлы (изображения)
│ └── categories/
├── static/ # Статические файлы
├── .env.example # Пример переменных окружения
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile # Docker образ приложения
├── manage.py # Django management скрипт
└── requirements.txt # Зависимости Python
```


## 🚀 Быстрый запуск

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd shop
cp .env.example .env
# Отредактируйте .env файл при необходимости