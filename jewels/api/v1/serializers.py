from rest_framework import serializers


class TopSerializer(serializers.Serializer):
    username = serializers.CharField(source='customer__username')
    spent_money = serializers.IntegerField()
    gems = serializers.ListField(source='gems_list')


class ResponseSerializer(serializers.Serializer):
    response = serializers.SerializerMethodField()

    def get_response(self, obj):
        return obj


class FileUploadSerializer(serializers.Serializer):
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
