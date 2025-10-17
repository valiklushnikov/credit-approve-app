from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PredictionConfig(models.Model):
    """
        Модель конфігурації режимів прогнозування.

        Зберігає активний режим роботи ML моделі для прогнозування
        схвалення кредитних заявок.

        Attributes:
            active_mode (CharField): Активний режим прогнозування
                - mode1: ModelA з історією кредиту
                - mode2: ModelB без історії кредиту
                - mode3: Ансамбль ModelA+ModelB
            updated_at (DateTimeField): Дата останнього оновлення
    """
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
    """
        Модель кредитної заявки користувача.

        Зберігає всю інформацію про заявку на кредит та результат
        прогнозування від ML моделі.

        Attributes:
            user (ForeignKey): Користувач, який подав заявку
            gender (CharField): Стать заявника
            married (CharField): Сімейний стан
            dependents (PositiveIntegerField): Кількість утриманців
            education (CharField): Рівень освіти
            self_employed (CharField): Чи є самозайнятим
            applicant_income (DecimalField): Дохід заявника
            coapplicant_income (DecimalField): Дохід співзаявника
            loan_amount (DecimalField): Сума кредиту
            loan_amount_term (PositiveIntegerField): Термін кредиту (місяці)
            credit_history (FloatField): Наявність кредитної історії (1.0/0.0)
            property_area (CharField): Тип місцевості (міська/передмістя/сільська)
            prediction_result (BooleanField): Результат прогнозування (схвалено/відхилено)
            created_at (DateTimeField): Дата створення заявки
    """
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
