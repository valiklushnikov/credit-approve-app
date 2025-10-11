from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.analytics, name="main"),
    path("collect-stats/", views.collect_stats_view, name="collect_stats"),
    path("<slug:graph>/", views.AnalyticGraphDetailView.as_view(), name="graph-detail"),
]
