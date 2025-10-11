import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def dependents_graph(df, output_dir, logger, images_dir):
    logger.info("7. Створення графіка утриманців...")
    plt.figure(figsize=(10, 7))
    dependents_approval = (
        df.groupby("Dependents")["Loan_Status"].value_counts(normalize=True).unstack()
        * 100
    )
    ax = dependents_approval.plot(kind="bar", color=["#e74c3c", "#2ecc71"], width=0.7)
    plt.title("Вплив кількості утриманців", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Кількість утриманців", fontsize=12)
    plt.ylabel("Процент (%)", fontsize=12)
    plt.legend(["Відмовлено", "Схвалено"], fontsize=11)
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=10)
    plt.tight_layout()
    file_name = "07_dependents.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="dependents_chart", defaults={"image_path": relative_path}
    )
