import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def pie_chart_graph(df, output_dir, logger, images_dir):
    logger.info("1. Створення pie chart...")
    plt.figure(figsize=(10, 8))
    approval_counts = df["Loan_Status"].value_counts()
    colors = ["#2ecc71", "#e74c3c"]
    plt.pie(
        approval_counts.values,
        labels=["Схвалено", "Відмовлено"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        textprops={"fontsize": 14},
    )
    plt.title("Розподіл схвалень кредиту", fontsize=16, fontweight="bold", pad=20)
    file_name = "01_loan_distribution.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="pie_chart", defaults={"image_path": relative_path}
    )
