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
git clone https://github.com/Laziz6066/Tafakkur_test.git
cd Tafakkur_test
cp .env.example .env
# Отредактируйте .env файл при необходимости
```

### 2. Запуск с Docker Compose
```bash
docker-compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000/api/

### 📊 Запущенные сервисы
#### После успешного запуска будут доступны:
#### API приложение: http://localhost:8000/api/
#### PostgreSQL: localhost:5433
#### Elasticsearch: http://localhost:9200
#### Kibana: http://localhost:5601 (для анализа Elasticsearch)
#### Swagger документация: http://localhost:8000/swagger/
#### ReDoc документация: http://localhost:8000/redoc/

## 🔧 Ручная установка (без Docker)
### 1. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Настройка базы данных
```
Создайте базу данных PostgreSQL
Отредактируйте DATABASE_URL в .env файле
```
### 3. Запуск Elasticsearch
```bash
# Установите и запустите Elasticsearch 8.12.2
# или используйте Docker:
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```
### 4. Миграции и запуск
```commandline
python manage.py migrate
python manage.py populate_es
python manage.py runserver
```
## 🔐 API Endpoints
### Аутентификация
```
POST /api/token/ - Получение JWT токенов
POST /api/token/refresh/ - Обновление access токена

```

### Категории (требуют аутентификации для записи)
```
GET /api/categories/ - Список категорий
POST /api/categories/ - Создание категории
GET /api/categories/{id}/ - Детали категории
PUT/PATCH /api/categories/{id}/ - Обновление категории
DELETE /api/categories/{id}/ - Удаление категории
```

### Товары (требуют аутентификации для записи)
```
GET /api/products/ - Список товаров
POST /api/products/ - Создание товара
GET /api/products/{id}/ - Детали товара
PUT/PATCH /api/products/{id}/ - Обновление товара
DELETE /api/products/{id}/ - Удаление товара
```

### Поиск (публичные)
```
GET /api/search/ - Полнотекстовый поиск товаров
GET /api/suggest/ - Автодополнение поисковых запросов
```


### 🧪 Тестирование
#### Запуск конкретных тестов
```bash
python manage.py test catalog.tests.test_authentication
python manage.py test catalog.tests.test_models
python manage.py test catalog.tests.test_serializers
python manage.py test catalog.tests.test_views
```
### Проверка качества кода
```bash
# Стиль кода в соответствии с Flake8
flake8 catalog/

# Импорты отсортированы с помощью Isort
isort --check-only catalog/
```
### 🛠️ Management команды
#### Индексация товаров в Elasticsearch
```bash
python manage.py populate_es
```
#### Ожидание готовности базы данных
```commandline
python manage.py wait_for_db
```
#### Создание суперпользователя
```commandline
python manage.py createsuperuser
```
### ⚙️ Конфигурация
#### Основные переменные окружения (.env)
```dotenv
DEBUG=1
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=*

# База данных
DATABASE_URL=postgres://user:password@db:5432/db_name

# Elasticsearch
ELASTICSEARCH_HOST=es
ELASTICSEARCH_PORT=9200

# Пагинация
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```
### 🔍 Поисковые возможности
#### Параметры поиска (/api/search/)

##### q - текстовый запрос
##### category - фильтр по категориям (через запятую)
##### price_min, price_max - диапазон цен
##### sort - сортировка (relevance, price_asc, price_desc)
##### page, page_size - пагинация
#### Пример запроса поиска
```bash
curl "http://localhost:8000/api/search/?q=смартфон&category=1,2&price_min=100&price_max=1000&sort=price_asc"
```
### 📈 Мониторинг
#### Elasticsearch: http://localhost:9200/_cluster/health
#### Kibana: http://localhost:5601 для визуализации данных
#### Django Admin: http://localhost:8000/admin/ для управления данными

### 📝 Дополнительная информация
#### Аутентификация: JWT tokens
#### База данных: PostgreSQL
#### Поиск: Elasticsearch
#### Документация: Swagger/ReDoc
#### Тестирование: Django Test Framework
#### Контейнеризация: Docker + Docker Compose
#### Для дополнительной информации обратитесь к документации API через Swagger UI.
