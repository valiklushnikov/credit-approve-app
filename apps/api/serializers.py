from rest_framework import serializers
from ml.data_transform import transform_input


class UserInfoWithoutCreditHistorySerializer(serializers.Serializer):
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

    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    married = serializers.ChoiceField(choices=MARRIED_CHOICES)
    dependents = serializers.IntegerField(min_value=0)
    education = serializers.ChoiceField(choices=EDUCATION_CHOICES)
    self_employed = serializers.ChoiceField(choices=SELF_EMPLOYED_CHOICES)
    applicant_income = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=0
    )
    coapplicant_income = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=0
    )
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    loan_amount_term = serializers.IntegerField(min_value=1)
    property_area = serializers.ChoiceField(choices=PROPERTY_AREA_CHOICES)

    class Meta:
        fields = (
            "gender",
            "married",
            "education",
            "self_employed",
            "applicant_income",
            "coapplicant_income",
            "loan_amount",
            "loan_amount_term",
            "property_area",
        )


class UserInfoWithCreditHistorySerializer(UserInfoWithoutCreditHistorySerializer):
    CREDIT_HISTORY_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]
    credit_history = serializers.ChoiceField(choices=CREDIT_HISTORY_CHOICES)

    class Meta(UserInfoWithoutCreditHistorySerializer.Meta):
        fields = UserInfoWithoutCreditHistorySerializer.Meta.fields + (
            "credit_history",
        )

    def validate_credit_history(self, value):
        mapping = {
            "Yes": 1.0,
            "No": 0.0,
        }
        return mapping[value]
