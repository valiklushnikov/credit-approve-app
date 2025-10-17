from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView

from . import models

from ml.analytics.analytics_creator import get_analytics


def analytics(request):
    """
        Представлення для відображення головної сторінки аналітики.

        Args:
            request: HTTP-запит

        Returns:
            HttpResponse: Відрендерений шаблон analytics/analytics.html
    """
    return render(request, "analytics/analytics.html")


class AnalyticGraphDetailView(DetailView):
    """
        Представлення для відображення детальної інформації про конкретний графік аналітики.

        Використовує поле 'name' як slug для ідентифікації графіка в URL.

        Атрибути:
            model: Модель AnalyticGraph
            context_object_name: Ім'я об'єкта в контексті шаблону ('graph')
            template_name: Шлях до шаблону для відображення
            slug_field: Поле моделі для використання як slug ('name')
            slug_url_kwarg: Назва параметра URL для slug ('graph')
    """
    model = models.AnalyticGraph
    context_object_name = "graph"
    template_name = "analytics/graph_detail.html"
    slug_field = "name"
    slug_url_kwarg = "graph"


def collect_stats_view(request):
    """
        Представлення для збору статистики та генерації графіків аналітики.

        Обробляє POST-запити для створення графіків аналітики через функцію get_analytics().
        При успішному створенні оновлює кеш та повертає JSON-відповідь.

        Args:
            request: HTTP-запит

        Returns:
            JsonResponse: JSON-відповідь зі статусом операції:
                - success: Графіки успішно створені
                - error: Виникла помилка при створенні або невірний тип запиту
    """
    if request.method == "POST":
        try:
            get_analytics()
            cache.set("graphics_exists", True, None)
            return JsonResponse(
                {"status": "success", "message": "Графіки аналітики успішно створені!"}
            )
        except:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Щось пішло не так при створенні графіків!",
                }
            )
    return JsonResponse({"status": "error", "message": "Невірний запит"})
