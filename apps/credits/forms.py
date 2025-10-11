from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .models import PredictionConfig, CreditApplication


class Step1Form(forms.Form):
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
    dependents = forms.IntegerField(
        label="Dependents",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "id": "dependents", "placeholder": " "}
        ),
        validators=[MinValueValidator(0)],
    )


class Step4Form(forms.Form):
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
        value = self.cleaned_data["prediction_result"]
        return bool(int(value))
