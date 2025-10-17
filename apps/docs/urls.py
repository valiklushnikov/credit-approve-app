from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "docs"

urlpatterns = [
    path("", RedirectView.as_view(url="/static/index.html", permanent=False)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
