from rest_framework import serializers
from ml.data_transform import transform_input


class UserInfoWithoutCreditHistorySerializer(serializers.Serializer):
    """
    Серіалізатор для даних користувача без кредитної історії (mode2).

    Використовується для валідації та обробки даних кредитної заявки
    в режимі прогнозування без урахування кредитної історії.

    Поля:
        gender: Стать заявника (Чоловік/Жінка)
        married: Сімейний стан (Одружений/Неодружений)
        dependents: Кількість утриманців (мінімум 0)
        education: Рівень освіти (Випускник/Не випускник)
        self_employed: Статус самозайнятості (Так/Ні)
        applicant_income: Дохід заявника (мінімум 0.00)
        coapplicant_income: Дохід співзаявника (мінімум 0.00)
        loan_amount: Сума кредиту (мінімум 0.00)
        loan_amount_term: Термін кредиту в місяцях (мінімум 1)
        property_area: Тип місцевості (Міська/Напівміська/Сільська)
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
    """
       Серіалізатор для даних користувача з кредитною історією (mode1).

       Розширює UserInfoWithoutCreditHistorySerializer додатковим полем
       для кредитної історії. Використовується в режимі прогнозування
       з урахуванням кредитної історії.

       Додаткові поля:
           credit_history: Наявність кредитної історії (Так/Ні)
    """
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
        """
            Перетворює текстове значення кредитної історії на числове.

            Args:
                value (str): Значення кредитної історії ("Yes" або "No")

            Returns:
                float: 1.0 для "Yes", 0.0 для "No"
        """
        mapping = {
            "Yes": 1.0,
            "No": 0.0,
        }
        return mapping[value]
