import pandas as pd
import numpy as np
import joblib
import os
from .data_transform import transform_input

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml_data")

MODEL_WITH_CH = os.path.join(MODEL_DIR, "best_model_with_credit_history.pkl")
MODEL_WITHOUT_CH = os.path.join(MODEL_DIR, "best_model_without_credit_history.pkl")


class EnsemblePredictor:
    """
        Клас для прогнозування схвалення кредитних заявок з використанням ансамблю ML моделей.

        Використовує дві попередньо навчені моделі:
            - model_B: модель з урахуванням кредитної історії (11 ознак)
            - model_A: модель без урахування кредитної історії (10 ознак + 4 додаткові)

        Підтримує три режими прогнозування:
            - mode1: Тільки model_B (з кредитною історією, поріг 0.5)
            - mode2: Тільки model_A (без кредитної історії, поріг 0.35)
            - mode3: Ансамбль обох моделей (усереднення ймовірностей, поріг 0.5)

        Attributes:
            model_B: Завантажена ML модель з кредитною історією
            model_A: Завантажена ML модель без кредитної історії
            features_B (list): Список ознак для model_B (11 ознак)
            features_A (list): Список ознак для model_A (10 базових ознак)

        Raises:
            FileNotFoundError: Якщо файли моделей не знайдено за вказаними шляхами
    """

    def __init__(self, model_with_ch_path: str, model_without_ch_path: str):
        """
            Ініціалізує EnsemblePredictor та завантажує ML моделі.

            Args:
                model_with_ch_path (str): Шлях до pkl файлу моделі з кредитною історією
                model_without_ch_path (str): Шлях до pkl файлу моделі без кредитної історії

            Raises:
                FileNotFoundError: Якщо будь-який з файлів моделей не існує
        """
        if not os.path.exists(model_with_ch_path):
            raise FileNotFoundError(f"Model not found: {model_with_ch_path}")
        if not os.path.exists(model_without_ch_path):
            raise FileNotFoundError(f"Model not found: {model_without_ch_path}")

        self.model_B = joblib.load(model_with_ch_path)
        self.model_A = joblib.load(model_without_ch_path)

        self.features_B = [
            "Gender",
            "Married",
            "Dependents",
            "Education",
            "Self_Employed",
            "ApplicantIncome",
            "CoapplicantIncome",
            "LoanAmount",
            "Loan_Amount_Term",
            "Credit_History",
            "Property_Area",
        ]
        self.features_A = [f for f in self.features_B if f != "Credit_History"]

    def _prepare_features_A(self, data: dict) -> pd.DataFrame:
        """
            Підготовує ознаки для моделі A з додатковими інженерними ознаками.

            Створює DataFrame з базовими ознаками та додає 4 нові розраховані ознаки:
                - Total_Income: Сумарний дохід заявника та співзаявника
                - Income_to_Loan: Співвідношення доходу до суми кредиту
                - Loan_per_Term: Сума кредиту на один місяць терміну
                - Is_Graduate_and_Employed: Бінарна ознака (випускник і не самозайнятий)

            Args:
                data (dict): Словник з трансформованими даними заявки

            Returns:
                pd.DataFrame: DataFrame з базовими та додатковими ознаками для моделі A
        """
        df = pd.DataFrame([data], columns=self.features_A)

        df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
        df["Income_to_Loan"] = df["Total_Income"] / (df["LoanAmount"] + 1)
        df["Loan_per_Term"] = df["LoanAmount"] / (df["Loan_Amount_Term"] + 1)
        df["Is_Graduate_and_Employed"] = np.where(
            (df["Education"] == "Graduate") & (df["Self_Employed"] == "No"), 1, 0
        )

        return df

    def predict(self, raw_data: dict, method: str = "mode3") -> int:
        """
            Виконує прогнозування схвалення кредитної заявки.

            Трансформує вхідні дані, підготовує ознаки для моделей та повертає
            бінарне рішення (0 - відхилено, 1 - схвалено) залежно від обраного методу.

            Args:
                raw_data (dict): Сирі дані заявки у форматі Django форм
                method (str, optional): Метод прогнозування. За замовчуванням "mode3"
                    - "mode1": Використовує тільки model_B (поріг 0.5)
                    - "mode2": Використовує тільки model_A (поріг 0.35)
                    - "mode3": Ансамбль обох моделей (поріг 0.5)

            Returns:
                int: Результат прогнозування (0 або 1)
                    - 0: Кредит відхилено
                    - 1: Кредит схвалено

            Raises:
                ValueError: Якщо method не є одним з: 'mode1', 'mode2', 'mode3'

            Example:
                >>> predictor = EnsemblePredictor(model_path1, model_path2)
                >>> data = {
                ...     "gender": "Male",
                ...     "married": "Yes",
                ...     "loan_amount": 150000.0,
                ...     ...
                ... }
                >>> result = predictor.predict(data, method="mode3")
                >>> print(result)  # 1 або 0
        """
        data = transform_input(raw_data)

        df_B = pd.DataFrame([data], columns=self.features_B)
        df_A = self._prepare_features_A(data)

        if method == "mode1":
            prob = self.model_B.predict_proba(df_B)[0][1]
            pred = int(prob >= 0.5)

        elif method == "mode2":
            prob = self.model_A.predict_proba(df_A)[0][1]
            pred = int(prob >= 0.35)

        elif method == "mode3":
            prob_A = self.model_A.predict_proba(df_A)[0][1]
            prob_B = self.model_B.predict_proba(df_B)[0][1]

            prob_final = (prob_A + prob_B) / 2
            pred = int(prob_final >= 0.5)
        else:
            raise ValueError("Method must be one of: 'mode1', 'mode2', 'mode3'")

        return pred
