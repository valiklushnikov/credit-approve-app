import os
from django.conf import settings
from django.core.cache import cache
from apps.analytics.models import AnalyticGraph
from apps.credits.models import PredictionConfig


def graphics_folder_exists():
    cached = cache.get("graphics_exists")
    if cached is not None:
        return cached

    exists = os.path.exists(os.path.join(settings.MEDIA_ROOT, "loan_analysis_plots"))

    if exists:
        cache.set("graphics_exists", True, None)

    return exists


def graphics(request):
    return {"graphics_exists": graphics_folder_exists()}


def analytics_graphs(request):
    graphs = AnalyticGraph.objects.all()
    return {"graphs": graphs}
