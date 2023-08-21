from rest_framework import serializers

from deals.models import Customer, Deal


class DealSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer.username'
    )

    class Meta:
        model = Deal
        fields = '__all__'


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

    expected_content_type = 'text/csv'

    deals = serializers.FileField()

    def validate_deals(self, value):
        try:
            if value.content_type == self.expected_content_type:
                return value
        except AttributeError as e:
            raise serializers.ValidationError(e)

        raise serializers.ValidationError(
            'Неверный тип файла. Ожидается CSV файл.'
        )
