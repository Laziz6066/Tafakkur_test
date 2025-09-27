from unittest.mock import Mock, patch


def mock_elasticsearch():
    """
    Создает mock объект для имитации Elasticsearch клиента в тестах.

    Используется для замены реального Elasticsearch
    клиента в тестовом окружении,
    чтобы избежать зависимостей от внешнего сервиса
    и ускорить выполнение тестов.

    Returns:
        Mock: Mock объект, имитирующий Elasticsearch
        клиент со следующими методами:
            - indices.exists: всегда возвращает False
            - indices.create: возвращает {'acknowledged': True}
            - indices.delete: возвращает {'acknowledged': True}

    Example:
        >>> es_mock = mock_elasticsearch()
        >>> es_mock.indices.exists('test_index')
        False
        >>> es_mock.indices.create(index='test_index')
        {'acknowledged': True}
    """

    mock_es = Mock()
    mock_es.indices = Mock()

    # Настройка mock методов для операций с индексами
    mock_es.indices.exists = Mock(return_value=False)
    mock_es.indices.create = Mock(return_value={'acknowledged': True})
    mock_es.indices.delete = Mock(return_value={'acknowledged': True})

    return mock_es


# Патч для импорта в тестах
elasticsearch_patch = patch(
    'catalog.documents.connections.get_connection',
    return_value=mock_elasticsearch())
