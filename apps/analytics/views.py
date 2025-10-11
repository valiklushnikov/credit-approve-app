from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView

from . import models

from ml.analytics.analytics_creator import get_analytics


def analytics(request):
    return render(request, "analytics/analytics.html")


class AnalyticGraphDetailView(DetailView):
    model = models.AnalyticGraph
    context_object_name = "graph"
    template_name = "analytics/graph_detail.html"
    slug_field = "name"
    slug_url_kwarg = "graph"


def collect_stats_view(request):
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
