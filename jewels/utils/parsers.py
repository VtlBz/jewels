from collections import defaultdict
import csv


def parse_deals(csv_file) -> dict:
    """
    Парсер данных о сделках из .csv файла.

    Построчно проходит по полученному файлу,
    формируя из записей в строке словарь с данными о сделке.

    Формат словаря: {'username': {'item': item, 'quantity': quantity,
    'total': total, 'deal_date': deal_date}},
    где username, item, total, quantity, deal_date -
    данные из строки из соответствующих колонок.
    Все сделки одного покупателя складываются в ключе с его username.
    """

    decoded_file = csv_file.read().decode('utf-8')
    reader = csv.reader(decoded_file.splitlines())

    objects = defaultdict(list)

    next(reader)
    for username, item, total, quantity, deal_date in reader:
        data = {'item': item,
                'quantity': quantity,
                'total': total,
                'deal_date': deal_date}
        if (not all(data.values())):
            raise ValueError('Невалидная строка. Некоторые элементы пусты.')
        objects[username].append(data)

    return objects
