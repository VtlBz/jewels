from django.contrib import admin
from django.db.models import Count, Sum

from deals.models import Customer, Deal


class DealInline(admin.TabularInline):
    model = Deal
    min_num = 1
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('customer')
        return queryset


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'deal_count', 'spent_money',)
    list_editable = ('username',)
    search_fields = ('username',)
    readonly_fields = ('deal_count', 'spent_money',)
    inlines = (DealInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).annotate(
            deal_count=Count('deals'),
            spent_money=Sum('deals__total')
        )
        return queryset

    def deal_count(self, obj):
        return obj.deal_count

    def spent_money(self, obj):
        return obj.spent_money

    deal_count.admin_order_field = 'deal_count'
    deal_count.short_description = 'Всего сделок'
    spent_money.admin_order_field = 'spent_money'
    spent_money.short_description = 'Всего потрачено'


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'customer', 'item', 'quantity', 'total', 'deal_date',
    )
    list_editable = ('total', 'quantity',)
    search_fields = ('customer__username', 'item',)
    list_filter = ('customer__username', 'item')

    def customer(self, obj):
        return obj.customer.username

    customer.short_description = Customer._meta.get_field(
        'username').verbose_name
