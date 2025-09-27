from django.conf import settings
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Обеспечивает преобразование данных категории в JSON и обратно.
    Включает валидацию уникальности имени категории.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "description", "image"]

    def validate_name(self, value):
        """
        Проверка уникальности имени категории.

        Args:
            value (str): Проверяемое имя категории

        Returns:
            str: Валидное имя категории

        Raises:
            ValidationError: Если категория с таким именем уже существует
        """
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Категория с таким именем уже существует"
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Включает дополнительное поле category_name для
    отображения названия категории.
    Обеспечивает валидацию цены и существования категории.
    """

    category_name = serializers.CharField(source="category.name",
                                          read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "category_name", "name",
                  "price", "image", "description"]

    def validate_category(self, value):
        """
        Проверка что категория существует.

        Args:
            value (Category): Проверяемая категория

        Returns:
            Category: Валидная категория

        Raises:
            ValidationError: Если категория не существует
        """
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Указанная "
                                              "категория не существует")
        return value

    def validate_price(self, value):
        """
        Проверка что цена положительная.

        Args:
            value (Decimal): Проверяемая цена

        Returns:
            Decimal: Валидная цена

        Raises:
            ValidationError: Если цена не положительная
        """
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value


class SearchQuerySerializer(serializers.Serializer):
    """
    Сериализатор для валидации параметров поиска товаров.

    Используется в ProductSearchView для проверки query-параметров.
    Поддерживает фильтрацию по тексту, категориям, цене и сортировку.
    """

    q = serializers.CharField(required=False, allow_blank=True, default="")
    category = serializers.CharField(required=False, allow_blank=True)
    price_min = serializers.DecimalField(required=False, max_digits=12,
                                         decimal_places=2, min_value=0)
    price_max = serializers.DecimalField(required=False, max_digits=12,
                                         decimal_places=2, min_value=0)

    SORT_CHOICES = ("relevance", "price_asc", "price_desc")
    sort = serializers.ChoiceField(required=False, choices=SORT_CHOICES,
                                   default="relevance")

    page = serializers.IntegerField(required=False, min_value=1, default=1)
    page_size = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=int(getattr(settings, "MAX_PAGE_SIZE", 100)),
        default=int(getattr(settings, "PAGE_SIZE", 20))
    )

    def validate_category(self, value):
        """
        Преобразование строки категорий в список ID.

        Args:
            value (str): Строка с ID категорий через запятую

        Returns:
            list: Список ID категорий

        Raises:
            ValidationError: Если формат строки некорректен
        """
        if value is None or value == "":
            return []
        try:
            ids = [int(x.strip()) for x in value.split(",") if x.strip()]
        except ValueError:
            raise serializers.ValidationError(
                "category must be a comma-separated list of integers")
        return ids

    def validate(self, attrs):
        """
        Валидация взаимосвязи параметров цены.

        Args:
            attrs (dict): Проверяемые атрибуты

        Returns:
            dict: Валидированные атрибуты

        Raises:
            ValidationError: Если price_min > price_max
        """
        price_min = attrs.get("price_min")
        price_max = attrs.get("price_max")
        if (price_min is not None and price_max is not None and
                price_min > price_max):
            raise serializers.ValidationError("price_min must "
                                              "be <= price_max")
        return attrs


class SuggestQuerySerializer(serializers.Serializer):
    """
    Сериализатор для валидации параметров автодополнения.

    Используется в ProductSuggestView для поисковых подсказок.
    """

    q = serializers.CharField(required=True, min_length=1)
    size = serializers.IntegerField(required=False, min_value=1,
                                    max_value=10, default=5)
