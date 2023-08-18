from rest_framework import serializers

from deals.models import Customer, Deal


class TopSerializer(serializers.Serializer):
    pass


class FileUploadSerializer(serializers.Serializer):
    expected_content_type = 'text/csv'

    deals = serializers.FileField()

    def validate_deals(self, attrs):
        content_type = self.initial_data['deals'].content_type
        if content_type != self.expected_content_type:
            raise serializers.ValidationError(
                'Неверный тип файла. Ожидается CSV файл.'
            )
        return super().validate(attrs)
