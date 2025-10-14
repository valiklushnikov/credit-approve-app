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

    def __init__(self, model_with_ch_path: str, model_without_ch_path: str):
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
        df = pd.DataFrame([data], columns=self.features_A)

        df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
        df["Income_to_Loan"] = df["Total_Income"] / (df["LoanAmount"] + 1)
        df["Loan_per_Term"] = df["LoanAmount"] / (df["Loan_Amount_Term"] + 1)
        df["Is_Graduate_and_Employed"] = np.where(
            (df["Education"] == "Graduate") & (df["Self_Employed"] == "No"), 1, 0
        )

        return df

    def predict(self, raw_data: dict, method: str = "mode3") -> int:
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
