from rest_framework import serializers


class TopSerializer(serializers.Serializer):
    """
    Сериализатор, формирующий данные о покупателе.

    Помещает данные о каждом покупателе в список в поле "response".
    """

    response = serializers.SerializerMethodField()

    def get_response(self, obj):
        return obj


class FileUploadSerializer(serializers.Serializer):
    """Сериализатор загрузки файла"""

    deals = serializers.FileField()

    def validate_deals(self, value):
        expected_content_type = 'text/csv'
        try:
            if value.content_type == expected_content_type:
                return value
        except AttributeError as e:
            raise serializers.ValidationError(e)

        raise serializers.ValidationError(
            'Неверный тип файла. Ожидается CSV файл.'
        )
