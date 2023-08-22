from collections import Counter, defaultdict
from itertools import chain


def processing_top_qs(queryset):
    """
    Обработчик данных в полученном кверисете.

    Выполняет обработку поля 'gems' для покупателя:
    Удаляет из списка дубликаты, затем формирует новый список,
    в котором присутствуют только предметы, имеющие пересечения
    хотя бы с одним другим покупателем в полученном наборе.
    """

    gems_data = {}
    for customer in queryset:
        gems_data[customer['username']] = customer['gems']
    counter = Counter(chain(*gems_data.values()))
    cross_gems = defaultdict(list)
    for customer, gems in gems_data.items():
        for gem in gems:
            if counter[gem] >= 2:
                cross_gems[customer].append(gem)
    for customer in queryset:
        customer['gems'] = cross_gems[customer['username']]

    return queryset
