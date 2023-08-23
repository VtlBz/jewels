from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.db import transaction
from django.db.models import Sum

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from deals.models import Customer
from utils import parse_deals, processing_top_qs
from .serializers import FileUploadSerializer, TopSerializer


cache_key_top = 'jewels-api-v1-deals-top-customers'


class DealsViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    Не задействован.

    Эндпоинт не используется в текущей версии сервиса.
    Является корневым для эндпоинтов `/top/` и `/upload/`
    """

    def get_serializer_class(self):
        if self.action == 'upload':
            return FileUploadSerializer

    def list(self, request, *args, **kwargs):
        absolute_url = request.build_absolute_uri()
        data = {'top': f'{absolute_url}top',
                'upload': f'{absolute_url}upload'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Загрузка файла с информацией о сделках.

        Формат файла: *.csv.
        Поля: 'customer', 'item', 'total', 'quantity', 'date'
        """

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = request.FILES.get('deals')
            try:
                parsed_data = parse_deals(csv_file)
            except ValueError as err:
                return Response(
                    data={'Status': 'Error',
                          'Desc': ('Не удалось обработать файл. '
                                   'Нарушена структура данных. '
                                   f'Ошибка: {err}')},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                for username, deals_data in parsed_data.items():
                    Customer.create_customer_with_deals(username, deals_data)
                with transaction.atomic():
                    Customer.objects.filter(is_actual=True).delete()
                    Customer.objects.all().update(is_actual=True)
                cache.delete(cache_key_top)
            except Exception as e:
                Customer.objects.filter(is_actual=False).delete()
                return Response(data={'Status': 'Error',
                                      'Desc': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(
                data={'Status': 'OK'},
                status=status.HTTP_200_OK
            )
        return Response(data={'Status': 'Error',
                              'Desc': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def top(self, request):
        """
        Получение ТОП-5 покупателей.

        В ответе отформатирован список покупок,
        и включает только покупки, имеющие вхождения
        в список покупок у других покупателей.
        """

        refresh = request.GET.get('refresh_cache') == 'true'

        if not cache.get(cache_key_top) or refresh:

            slice = settings.TOP_CUSTOMERS_COUNT
            queryset = Customer.objects.values('username').annotate(
                gems=ArrayAgg('deals__item', distinct=True),
                spent_money=Sum('deals__total')
            ).order_by('-spent_money')[:slice]
            formatted_qs = processing_top_qs(queryset)
            serializer = TopSerializer(formatted_qs)

            cache.set(cache_key_top, serializer.data, timeout=None)

        return Response(cache.get(cache_key_top))
