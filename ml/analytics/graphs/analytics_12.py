import os
import pandas as pd
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_classif


def mutual_score_graph(df, output_dir, logger, images_dir):
    logger.info("12. Створення графіка Mutual Information...")
    plt.figure(figsize=(12, 8))
    le = LabelEncoder()
    X_encoded = df.copy()
    categorical_cols = [
        "Gender",
        "Married",
        "Education",
        "Self_Employed",
        "Property_Area",
    ]
    for col in categorical_cols:
        X_encoded[col] = le.fit_transform(X_encoded[col])

    features_for_mi = [
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

    X_mi = X_encoded[features_for_mi]
    mi_scores = mutual_info_classif(
        X_mi, X_encoded["Loan_Status_Binary"], random_state=42
    )

    mi_results = pd.DataFrame(
        {"Feature": features_for_mi, "MI_Score": mi_scores}
    ).sort_values("MI_Score", ascending=True)

    colors_mi = plt.cm.RdYlGn(
        mi_results["MI_Score"].values / mi_results["MI_Score"].max()
    )
    plt.barh(mi_results["Feature"], mi_results["MI_Score"], color=colors_mi)
    plt.title(
        "Mutual Information Score - Важливість ознак",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("MI Score", fontsize=12)
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    file_name = "12_mutual_information.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="mutual_information", defaults={"image_path": relative_path}
    )
