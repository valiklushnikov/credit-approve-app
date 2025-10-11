import os
import pandas as pd
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency


def chi_square_graph(df, output_dir, logger, images_dir):
    logger.info("11. Створення графіка Chi-square...")
    plt.figure(figsize=(12, 8))
    categorical_features = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area",
        "Credit_History",
    ]
    chi_square_results = []
    for feature in categorical_features:
        contingency_table = pd.crosstab(df[feature], df["Loan_Status"])
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        chi_square_results.append(
            {"Feature": feature, "Chi2": chi2, "P-value": p_value}
        )

    chi_df = pd.DataFrame(chi_square_results).sort_values("Chi2", ascending=True)
    colors_chi = [
        "#2ecc71" if x < 0.05 else "#e74c3c" for x in chi_df["P-value"].values
    ]
    plt.barh(chi_df["Feature"], chi_df["Chi2"], color=colors_chi)
    plt.title(
        "Chi-square статистика\n (Зелений = статистично значущий, p <0.05)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Chi-square значення", fontsize=12)
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    file_name = "11_chi_square.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="chi_square_graph", defaults={"image_path": relative_path}
    )
