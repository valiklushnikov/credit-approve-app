import matplotlib
import os

from apps.analytics.models import AnalyticGraph

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def property_area_graph(df, output_dir, logger, images_dir):
    logger.info("5. Створення графіка розташування...")
    plt.figure(figsize=(10, 7))
    property_approval = (
        df.groupby("Property_Area")["Loan_Status"]
        .value_counts(normalize=True)
        .unstack()
        * 100
    )
    ax = property_approval.plot(kind="bar", color=["#e74c3c", "#2ecc71"], width=0.7)
    plt.title("Вплив розташування нерухомості", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Розташування", fontsize=12)
    plt.ylabel("Процент (%)", fontsize=12)
    plt.legend(["Відмовлено", "Схвалено"], fontsize=11)
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=10)
    plt.tight_layout()
    file_name = "05_property_area.png"
    plt.savefig(os.path.join(output_dir, file_name), dpi=150, bbox_inches="tight")
    plt.close()
    relative_path = os.path.join(images_dir, file_name)
    AnalyticGraph.objects.get_or_create(
        name="location_chart", defaults={"image_path": relative_path}
    )
