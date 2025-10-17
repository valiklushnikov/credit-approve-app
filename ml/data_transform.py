from decimal import Decimal


def transform_input(raw_data: dict) -> dict:
    """
        Перетворює вхідні дані з формату форм Django в формат для ML моделі.

        Функція виконує маппінг назв полів з snake_case (використовується у формах)
        на назви колонок датасету ML моделі. Також конвертує Decimal значення в float.

        Args:
            raw_data (dict): Словник з даними у форматі форм Django
                Приклад: {"gender": "Male", "loan_amount": Decimal("150000.00"), ...}

        Returns:
            dict: Словник з трансформованими назвами полів та значеннями
                Приклад: {"Gender": "Male", "LoanAmount": 150000.0, ...}

        Note:
            - Ігнорує поля, які відсутні в маппінгу
            - Автоматично конвертує Decimal у float для сумісності з ML моделлю
    """
    mapping = {
        "gender": "Gender",
        "married": "Married",
        "dependents": "Dependents",
        "education": "Education",
        "self_employed": "Self_Employed",
        "applicant_income": "ApplicantIncome",
        "coapplicant_income": "CoapplicantIncome",
        "loan_amount": "LoanAmount",
        "loan_amount_term": "Loan_Amount_Term",
        "credit_history": "Credit_History",
        "property_area": "Property_Area",
    }

    transformed = {}

    for key, value in raw_data.items():
        if key not in mapping:
            continue

        if isinstance(value, Decimal):
            value = float(value)
        transformed[mapping[key]] = value

    return transformed
