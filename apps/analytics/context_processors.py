from django.core.cache import cache
from apps.analytics.models import AnalyticGraph


def analytics_graphs(request):
    """
        Контекстний процесор для додавання графіків аналітики до контексту шаблонів.

        Отримує список графіків з кешу або з бази даних, якщо кеш порожній.
        Кешує результат без обмеження за часом.

        Args:
            request: HTTP-запит

        Returns:
            dict: Словник з ключем 'graphs', що містить список об'єктів AnalyticGraph
    """
    graphs = cache.get("analytics_graphs")
    if not graphs:
        graphs = list(AnalyticGraph.objects.all())
        cache.set("analytics_graphs", graphs, None)
    return {"graphs": graphs}
