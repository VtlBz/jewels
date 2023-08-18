import csv

from django.db import transaction

from deals.models import Customer, Deal


@transaction.atomic
def parse_deals(csv_file):
    decoded_file = csv_file.read().decode('utf-8')
    reader = csv.reader(decoded_file.splitlines())

    next(reader)
    for username, item, total, quantity, deal_date in reader:
        customer, created = Customer.objects.get_or_create(
            username=username
        )
        if created:
            customer.save()

        deal = Deal.objects.create(customer=customer,
                                   item=item,
                                   quantity=quantity,
                                   total=total,
                                   deal_date=deal_date)
        deal.save()
