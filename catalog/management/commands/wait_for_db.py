import os
import time
from urllib.parse import urlparse

import psycopg2
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Management command для ожидания готовности базы данных PostgreSQL.

    Команда периодически проверяет доступность базы данных
    перед запуском приложения.
    Используется в Docker Compose для обеспечения правильного
    порядка запуска сервисов.

    Особенности:
    - Бесконечный цикл проверки подключения
    - Экспоненциальная задержка между попытками (опционально)
    - Чтение параметров подключения из переменных окружения
    - Детальное логирование процесса подключения

    Использование в docker-compose:
        command: >
            sh -c "
            python manage.py wait_for_db &&
            python manage.py migrate &&
            python manage.py runserver
            "
    """

    help = "Wait for Postgres to be available"

    def handle(self, *args, **options):
        """
        Основной метод выполнения команды.

        Выполняет попытки подключения к базе данных до успешного соединения.
        При неудачной попытке выводит сообщение об ошибке и
        повторяет через 1 секунду.

        Args:
            *args: Дополнительные аргументы
            **options: Опции команды

        Returns:
            None

        Raises:
            KeyError: Если переменная окружения DATABASE_URL не установлена

        Process:
            1. Чтение DATABASE_URL из переменных окружения
            2. Парсинг URL для извлечения параметров подключения
            3. Попытка установить соединение с PostgreSQL
            4. При успехе - вывод сообщения и завершение
            5. При ошибке - пауза и повторная попытка

        Example output:
            DB not ready: connection to server at "localhost"
            (::1), port 5432 failed
            DB not ready: connection to server at "localhost"
            (::1), port 5432 failed
            Database is ready.
        """

        # Получение URL базы данных из переменных окружения
        url = os.environ["DATABASE_URL"]
        p = urlparse(url)

        self.stdout.write("Waiting for database to be ready...")
        self.stdout.write(f"Host: {p.hostname}, Port: {p.port}, "
                          f"Database: {p.path[1:]}")

        attempt = 1
        max_attempts = 30  # Максимальное количество попыток

        while attempt <= max_attempts:
            try:
                # Попытка установить соединение с базой данных
                conn = psycopg2.connect(
                    dbname=p.path[1:],
                    user=p.username,
                    password=p.password,
                    host=p.hostname,
                    port=p.port,
                    connect_timeout=5  # Таймаут подключения 5 секунд
                )
                conn.close()

                # Успешное подключение
                self.stdout.write(
                    self.style.SUCCESS("Database is ready and "
                                       "accepting connections.")
                )
                break

            except Exception as e:
                # Ошибка подключения
                self.stdout.write(
                    f"Attempt {attempt}/{max_attempts}: "
                    f"Database not ready - {e}"
                )

                # Проверка достижения максимального количества попыток
                if attempt >= max_attempts:
                    self.stdout.write(
                        self.style.ERROR("Max attempts reached. Exiting.")
                    )
                    raise

                # Увеличение задержки с каждой попыткой
                # (экспоненциальная backoff)
                delay = min(2 ** attempt, 10)  # Максимальная
                # задержка 10 секунд
                self.stdout.write(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                attempt += 1
