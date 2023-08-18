from django.conf import settings
from django.db.models import Count, OuterRef, Prefetch, Sum

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from deals.models import Customer, Deal
from utils.parse_deals import parse_deals
from .serializers import FileUploadSerializer, TopSerializer


class TopViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TopSerializer

    def get_queryset(self):
        slice = settings.TOP_CUSTOMERS_COUNT
        top_customers = Deal.objects.values('customer').annotate(spent_money=Sum('total')).order_by('-spent_money')[:slice]
        for c in top_customers:
            print(type(c))
        print(top_customers)
        gem_list = Deal.objects.filter(
            customer__in=[customer['customer'] for customer in top_customers]
        ).values('item').annotate(
            count=Count('customer')).filter(count__gte=2).values_list('item', flat=True)
        print(gem_list)
        queryset = super().get_queryset()
    #     # .annotate(
    #     #     deal_count=Count('deals'),
    #     #     spent_money=Sum('deals__total')
    #     # )
        return queryset

    # pass
    # @action(detail=False, methods=['get'])
    # def top(self, request):
    #     data = {'message': 'Эндпоинт "ТОП" работает'}
    #     serializer = DealSerializer()

    #     return Response(data=serializer.data,
    #                     status=status.HTTP_200_OK)


class DealsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = request.FILES.get('deals')
            if parse_deals(csv_file):
                return Response(
                    data={'status': 'OK - файл был обработан без ошибок'},
                    status=status.HTTP_200_OK
                )
        return Response(data={'Ошибка': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
