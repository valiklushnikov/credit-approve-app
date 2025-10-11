from decimal import Decimal


def transform_input(raw_data: dict) -> dict:
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
