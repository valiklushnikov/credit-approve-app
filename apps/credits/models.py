from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PredictionConfig(models.Model):
    MODE_CHOICES = [
        ("mode1", "ModelA with credit history"),
        ("mode2", "ModelB without credit history"),
        ("mode3", "ModelA+ModelB"),
    ]

    active_mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default="mode1",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Current mode: {self.active_mode}"



class CreditApplication(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    MARRIED_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    EDUCATION_CHOICES = [
        ("Graduate", "Graduate"),
        ("Not Graduate", "Not Graduate"),
    ]

    SELF_EMPLOYED_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    PROPERTY_AREA_CHOICES = [
        ("Urban", "Urban"),
        ("Semiurban", "Semiurban"),
        ("Rural", "Rural"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credits")
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    married = models.CharField(
        max_length=5,
        choices=MARRIED_CHOICES
    )
    dependents = models.PositiveIntegerField()
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES
    )
    self_employed = models.CharField(
        max_length=5,
        choices=SELF_EMPLOYED_CHOICES
    )
    applicant_income = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    coapplicant_income = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    loan_amount_term = models.PositiveIntegerField()
    credit_history = models.FloatField(blank=True, null=True)
    property_area = models.CharField(
        max_length=20,
        choices=PROPERTY_AREA_CHOICES
    )

    prediction_result = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} ({self.prediction_result})"
