from collections import Counter, defaultdict
from itertools import chain


def processing_top_qs(queryset):
    """
    Обработчик данных в полученном кверисете.

    Выполняет обработку поля 'gems_list' для покупателя:
    Удаляет из списка дубликаты, затем формирует новый список,
    в котором присутствуют только предметы, имеющие пересечения
    хотя бы с одним другим покупателем в полученном наборе.
    """
    unique_gems_data = {}
    for item in queryset:
        unique_gems_data[item['username']] = set(item['gems'])
    c = Counter(chain(*unique_gems_data.values()))
    result_gems = defaultdict(list)
    for customer, items in unique_gems_data.items():
        for item in items:
            if c[item] >= 2:
                result_gems[customer].append(item)
    for item in queryset:
        item['gems'] = result_gems[item['username']]

    return queryset
