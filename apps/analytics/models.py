from django.db import models


class AnalyticGraph(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    @property
    def templates_name(self):
        return " ".join(self.name.split("_")).title()

    @property
    def image_url(self):
        from django.conf import settings

        return f"{settings.MEDIA_URL}{self.image_path}"
