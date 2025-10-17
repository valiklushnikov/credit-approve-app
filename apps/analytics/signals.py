from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from apps.analytics.models import AnalyticGraph

@receiver([post_save, post_delete], sender=AnalyticGraph)
def clear_analytics_graphs(sender, **kwargs):
    """
        Очищує кеш графіків аналітики після збереження або видалення.

        Сигнал спрацьовує при збереженні або видаленні об'єкта AnalyticGraph
        та очищає весь кеш для оновлення даних.

        Args:
            sender: Модель, яка викликала сигнал
            **kwargs: Додаткові аргументи сигналу
    """
    if sender.name != "apps.analytics":
        return
    cache.clear()
