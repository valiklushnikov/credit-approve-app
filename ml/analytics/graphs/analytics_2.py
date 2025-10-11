import os
import seaborn as sns
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def correlation(df, output_dir, logger, images_dir):
    logger.info("2. Створення кореляційної матриці...")
    plt.figure(figsize=(12, 10))
    numerical_for_corr = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Dependents",
    ]
    correlation_matrix = df[numerical_for_corr + ["Loan_Status_Binary"]].corr()
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        cbar_kws={"label": "Кореляція"},
        square=True,
        linewidths=1,
    )
    plt.title(
        "Кореляційна матриця числових ознак", fontsize=16, fontweight="bold", pad=20
    )
    plt.tight_layout()
    file_name = "02_correlation_matrix.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="correlation_matrix", defaults={"image_path": relative_path}
    )
    return correlation_matrix
