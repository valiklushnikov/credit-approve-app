from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .models import PredictionConfig, CreditApplication


class Step1Form(forms.Form):
    """
        Форма першого кроку: вибір статі заявника.

        Поля:
            gender: Стать заявника (Чоловік/Жінка)
    """
    gender = forms.ChoiceField(
        label="Gender",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "gender",
                "placeholder": " ",
            }
        ),
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
    )


class Step2Form(forms.Form):
    """
       Форма другого кроку: вибір сімейного стану заявника.

       Поля:
           married: Сімейний стан (Одружений/Неодружений)
    """
    married = forms.ChoiceField(
        label="Married",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "married",
                "placeholder": " ",
            }
        ),
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
    )


class Step3Form(forms.Form):
    """
       Форма третього кроку: вказання кількості утриманців.

       Поля:
           dependents: Кількість утриманців (мінімум 0)
    """
    dependents = forms.IntegerField(
        label="Dependents",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "id": "dependents", "placeholder": " "}
        ),
        validators=[MinValueValidator(0)],
    )


class Step4Form(forms.Form):
    """
       Форма четвертого кроку: вибір рівня освіти заявника.

       Поля:
           education: Рівень освіти (Випускник/Не випускник)
    """
    education = forms.ChoiceField(
        label="Education",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "education",
                "placeholder": " ",
            }
        ),
        choices=[
            ("Graduate", "Graduate"),
            ("Not Graduate", "Not Graduate"),
        ],
    )


class Step5Form(forms.Form):
    """
        Форма п'ятого кроку: вказання статусу самозайнятості.

        Поля:
            self_employed: Чи є заявник самозайнятим (Так/Ні)
    """
    self_employed = forms.ChoiceField(
        label="Self Employed",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "self-employed",
                "placeholder": " ",
            }
        ),
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
    )


class Step6Form(forms.Form):
    """
        Форма шостого кроку: вказання доходу заявника.

        Поля:
            applicant_income: Дохід заявника (мінімум 0.00)
    """
    applicant_income = forms.DecimalField(
        label="Applicant Income",
        required=True,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "applicant-income",
                "placeholder": " ",
                "step": "0.01",
            }
        ),
        validators=[MinValueValidator(Decimal("0.00"))],
    )


class Step7Form(forms.Form):
    """
       Форма сьомого кроку: вказання доходу співзаявника.

       Поля:
           coapplicant_income: Дохід співзаявника (мінімум 0.00)
    """
    coapplicant_income = forms.DecimalField(
        label="CoApplicant Income",
        required=True,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "co-applicant-income",
                "placeholder": " ",
                "step": "0.1",
            }
        ),
        validators=[MinValueValidator(Decimal("0.00"))],
    )


class Step8Form(forms.Form):
    """
      Форма восьмого кроку: вказання суми кредиту.

      Поля:
          loan_amount: Сума кредиту (мінімум 0.00)
    """
    loan_amount = forms.DecimalField(
        label="Loan Amount",
        required=True,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "loan-amount",
                "placeholder": " ",
                "step": "0.01",
            }
        ),
        validators=[MinValueValidator(Decimal("0.00"))],
    )


class Step9Form(forms.Form):
    """
        Форма дев'ятого кроку: вказання терміну кредиту.

        Поля:
            loan_amount_term: Термін кредиту в місяцях (від 0 до 360)
    """
    loan_amount_term = forms.IntegerField(
        label="Loan Amount Term",
        required=True,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "loan-amount-term",
                "placeholder": " ",
            }
        ),
        validators=[MinValueValidator(0), MaxValueValidator(360)],
    )


class Step10Form(forms.Form):
    """
        Форма десятого кроку: вказання кредитної історії.

        Поля:
            credit_history: Наявність кредитної історії (1.0 - є, 0.0 - немає)
    """
    credit_history = forms.TypedChoiceField(
        label="Credit History",
        required=True,
        choices=[
            (1.0, "You have credit history"),
            (0.0, "You have not credit history"),
        ],
        coerce=float,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "credit-history",
                "placeholder": " ",
            }
        ),
    )


class Step11Form(forms.Form):
    """
        Форма одинадцятого кроку: вибір місцезнаходження нерухомості.

        Поля:
            property_area: Тип місцевості (Сільська/Міська/Напівміська)
    """
    property_area = forms.ChoiceField(
        label="Property Area",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "property-area",
                "placeholder": " ",
            }
        ),
        choices=[
            ("Rural", "Rural"),
            ("Urban", "Urban"),
            ("Semiurban", "Semiurban"),
        ],
    )


class PredictionConfigForm(forms.ModelForm):
    """
        Форма для налаштування конфігурації прогнозування.

        Дозволяє адміністратору змінювати активний режим роботи системи прогнозування.

        Поля:
            active_mode: Активний режим роботи системи, за замовчуванням "mode1".
    """
    active_mode = forms.ChoiceField(
        label="Active Mode",
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "form-active-mode",
                "placeholder": " ",
            }
        ),
        choices=PredictionConfig.MODE_CHOICES,
    )

    class Meta:
        model = PredictionConfig
        fields = ["active_mode"]


class UpdateStatusForm(forms.ModelForm):
    """
       Форма для оновлення статусу кредитної заявки.

       Дозволяє адміністратору змінювати результат прогнозування заявки
       (скасовано або завершено).

       Поля:
           prediction_result: Статус заявки (0 - Скасовано, 1 - Завершено)
    """
    prediction_result = forms.ChoiceField(
        label="Order Status",
        widget=forms.Select(
            attrs={
                "class": "form-control text-center",
                "id": "form-status-update",
                "placeholder": " ",
            }
        ),
        choices=[
            (0, "Cancelled"),
            (1, "Completed"),
        ],
    )

    class Meta:
        model = CreditApplication
        fields = ["prediction_result"]

    def clean_prediction_result(self):
        """
            Перетворює значення статусу заявки на булеве значення.

            Returns:
                bool: True для завершеної заявки, False для скасованої
        """
        value = self.cleaned_data["prediction_result"]
        return bool(int(value))
