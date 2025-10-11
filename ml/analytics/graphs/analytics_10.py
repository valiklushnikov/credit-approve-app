import os
import matplotlib

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def total_income_graph(df, output_dir, logger, images_dir):
    logger.info("10. Створення графіка категорій доходу...")
    plt.figure(figsize=(10, 7))
    df["Income_Category"] = pd.cut(
        df["Total_Income"],
        bins=[0, 5000, 10000, 20000, float("inf")],
        labels=["Низький", "Середній", "Високий", "Дуже високий"],
    )
    income_approval = (
        df.groupby("Income_Category")["Loan_Status"]
        .value_counts(normalize=True)
        .unstack()
        * 100
    )
    ax = income_approval.plot(kind="bar", color=["#e74c3c", "#2ecc71"], width=0.7)
    plt.title("Вплив категорії доходу", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Категорія доходу", fontsize=12)
    plt.ylabel("Процент (%)", fontsize=12)
    plt.legend(["Відмовлено", "Схвалено"], fontsize=11)
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=10)
    plt.tight_layout()
    file_name = "10_income_category.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="income_category_chart", defaults={"image_path": relative_path}
    )
