from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.db import transaction
from django.db.models import Sum
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from deals.models import Customer, Deal
from utils import parse_deals, processing_top_qs
from .serializers import (
    FileUploadSerializer, ResponseSerializer, TopSerializer,
)


class DealsViewSet(viewsets.ReadOnlyModelViewSet):

    @swagger_auto_schema()
    @action(detail=False, methods=['post'])
    def upload(self, request):
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
                cache.clear()
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

    @swagger_auto_schema()
    @method_decorator(cache_page(None))
    @action(detail=False, methods=['get'])
    def top(self, request):
        slice = settings.TOP_CUSTOMERS_COUNT
        queryset = Deal.objects.values('customer__username').annotate(
            gems_list=ArrayAgg('item'), spent_money=Sum('total')
        ).order_by('-spent_money')[:slice]
        queryset = processing_top_qs(queryset)
        serializer = ResponseSerializer(
            TopSerializer(queryset, many=True).data
        )
        return Response(serializer.data)
