import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def married_graph(df, output_dir, logger, images_dir):
    logger.info("4. Створення графіка сімейного стану...")
    plt.figure(figsize=(10, 7))
    marriage_approval = (
        df.groupby("Married")["Loan_Status"].value_counts(normalize=True).unstack()
        * 100
    )
    ax = marriage_approval.plot(kind="bar", color=["#e74c3c", "#2ecc71"], width=0.7)
    plt.title("Вплив сімейного стану", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Сімейний стан", fontsize=12)
    plt.ylabel("Процент (%)", fontsize=12)
    plt.legend(["Відмовлено", "Схвалено"], fontsize=11)
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=10)
    plt.tight_layout()
    file_name = "04_marital_status.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="marital_status_chart", defaults={"image_path": relative_path}
    )
