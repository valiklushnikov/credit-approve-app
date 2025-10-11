from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.credits.models import PredictionConfig


@receiver(post_migrate)
def create_prediction_mode(sender, **kwargs):
    if sender.name != "apps.credits":
        return
    PredictionConfig.objects.get_or_create(id=1, defaults={"active_mode": "mode1"})
