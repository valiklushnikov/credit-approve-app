import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def correlation_matrix_graph(output_dir, correlation_matrix, logger, images_dir):
    logger.info("9. Створення графіка кореляцій...")
    plt.figure(figsize=(12, 8))
    loan_correlations = correlation_matrix["Loan_Status_Binary"].drop(
        "Loan_Status_Binary"
    )
    loan_correlations_sorted = loan_correlations.sort_values()
    colors_corr = [
        "#e74c3c" if x < 0 else "#2ecc71" for x in loan_correlations_sorted.values
    ]
    plt.barh(
        loan_correlations_sorted.index,
        loan_correlations_sorted.values,
        color=colors_corr,
    )
    plt.title(
        "Кореляція ознак із схваленням кредиту", fontsize=16, fontweight="bold", pad=20
    )
    plt.xlabel("Коефіцієнт кореляції", fontsize=12)
    plt.axvline(x=0, color="black", linestyle="-", linewidth=1)
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    file_name = "09_correlation_bar.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="correlation_bar", defaults={"image_path": relative_path}
    )
