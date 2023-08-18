from django.core.validators import MinValueValidator
from django.db import models


class Customer(models.Model):
    """Модель покупателя"""

    username = models.CharField(
        max_length=200,
        verbose_name='Покупатель',
    )

    class Meta:
        db_table = 'Customers'
        verbose_name = 'Покупатели'
        verbose_name_plural = 'Покупатели'

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
        db_table = 'Deals'
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return (f'[{self.customer} -> {self.item}]: '
                f'{self.deal_date}, {self.quantity}, {self.total}')
