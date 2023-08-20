from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Customer(models.Model):
    """
    Модель покупателя.

    Содержит данные о покупателе.
    В поле is_actual содержится отметка
    об актуальности записи для целей обеспечения версионизаци и данных.
    """

    username = models.CharField(
        max_length=200,
        verbose_name='Покупатель',
    )
    is_actual = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'customers'
        verbose_name = 'Покупатели'
        verbose_name_plural = 'Покупатели'

    @classmethod
    def create_customer_with_deals(cls, username, deals_data) -> None:
        """
        Метод для создания объекта Customer,
        с привязкой к нему сделок из полученного списка сделок.
        """

        customer = cls.objects.create(username=username)
        deals_objs = Deal.make_deals_list(customer, deals_data)
        Deal.objects.bulk_create(
            deals_objs, batch_size=settings.BULK_CREATE_BATCH_SIZE
        )

    def __str__(self):
        return f'{self.username}'


class Deal(models.Model):
    """Модель сделок"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name='Покупатель'
    )
    item = models.CharField(
        max_length=100,
        verbose_name='Драгоценный камень',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество товара',
        validators=[
            MinValueValidator(
                1, 'Количество товара не может быть меньше 1!'
            ),
        ],
        default=1,
    )
    total = models.PositiveIntegerField(
        verbose_name='Сумма сделки',
        validators=[
            MinValueValidator(
                1, 'Сумма сделки не может быть меньше 1!'
            ),
        ],
        default=1,
    )
    deal_date = models.DateTimeField(
        verbose_name='Дата сделки',
    )

    class Meta:
        db_table = 'deals'
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    @classmethod
    def make_deals_list(cls, customer, deals_data) -> list:
        """
        Метод для создания списка объектов Deal
        для последующего пакетного сохранения.
        """

        deal_objs = []
        for deal in deals_data:
            deal_objs.append(
                cls(customer=customer,
                    item=deal['item'],
                    quantity=deal['quantity'],
                    total=deal['total'],
                    deal_date=deal['deal_date'])
            )
        return deal_objs

    def __str__(self):
        return (f'[{self.customer} -> {self.item}]: '
                f'{self.quantity}, {self.total}, {self.deal_date}')
