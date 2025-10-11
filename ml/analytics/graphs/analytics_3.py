import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def credit_history_graph(df, output_dir, logger, images_dir):
    logger.info("3. Створення графіка кредитної історії...")
    plt.figure(figsize=(10, 7))
    credit_approval = (
        df.groupby("Credit_History")["Loan_Status"]
        .value_counts(normalize=True)
        .unstack()
        * 100
    )
    ax = credit_approval.plot(kind="bar", color=["#e74c3c", "#2ecc71"], width=0.7)
    plt.title(
        "Вплив кредитної історії на схвалення", fontsize=16, fontweight="bold", pad=20
    )
    plt.xlabel("Кредитна історія (0=Погана, 1=Хороша)", fontsize=12)
    plt.ylabel("Процент (%)", fontsize=12)
    plt.legend(["Відмовлено", "Схвалено"], fontsize=11)
    plt.xticks(rotation=0)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=10)
    plt.tight_layout()
    file_name = "03_credit_history.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="credit_history_chart", defaults={"image_path": relative_path}
    )
