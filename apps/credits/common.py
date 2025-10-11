from . import forms

TEMPLATES = {
        "gender": "credits/stepper/steps/step1.html",
        "married": "credits/stepper/steps/step2.html",
        "dependents": "credits/stepper/steps/step3.html",
        "education": "credits/stepper/steps/step4.html",
        "self_employed": "credits/stepper/steps/step5.html",
        "applicant_income": "credits/stepper/steps/step6.html",
        "coapplicant_income": "credits/stepper/steps/step7.html",
        "loan_amount": "credits/stepper/steps/step8.html",
        "loan_amount_term": "credits/stepper/steps/step9.html",
        "credit_history": "credits/stepper/steps/step10.html",
        "property_area": "credits/stepper/steps/step11.html",
    }

FORMS = [
        ("gender", forms.Step1Form),
        ("married", forms.Step2Form),
        ("dependents", forms.Step3Form),
        ("education", forms.Step4Form),
        ("self_employed", forms.Step5Form),
        ("applicant_income", forms.Step6Form),
        ("coapplicant_income", forms.Step7Form),
        ("loan_amount", forms.Step8Form),
        ("loan_amount_term", forms.Step9Form),
        ("credit_history", forms.Step10Form),
        ("property_area", forms.Step11Form),
    ]