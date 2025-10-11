import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import sys

import django


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


django.setup()

from django.conf import settings

warnings.filterwarnings("ignore")
from . import graphs


import logging
import os

log_file = os.path.join(project_root, "ml", "loan_analysis.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)


file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)


def get_analytics():
    images_dir = "loan_analysis_plots"
    output_dir = os.path.join(settings.MEDIA_ROOT, images_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(os.path.join(project_root, "ml", "loan_data.csv"))

    categorical_columns = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area",
    ]
    numerical_columns = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
    ]

    for col in categorical_columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    for col in numerical_columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    df["Dependents"] = df["Dependents"].replace("3+", "3").astype(int)
    df["Loan_Status_Binary"] = df["Loan_Status"].map({"Y": 1, "N": 0})
    df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]

    sns.set_style("whitegrid")
    plt.rcParams["font.size"] = 11

    root_logger.info("Починаю створення графіків...")
    root_logger.info("=" * 50)

    graphs.pie_chart_graph(df, output_dir, root_logger, images_dir)
    corr_matrix = graphs.correlation(df, output_dir, root_logger, images_dir)
    graphs.credit_history_graph(df, output_dir, root_logger, images_dir)
    graphs.married_graph(df, output_dir, root_logger, images_dir)
    graphs.property_area_graph(df, output_dir, root_logger, images_dir)
    graphs.education_graph(df, output_dir, root_logger, images_dir)
    graphs.dependents_graph(df, output_dir, root_logger, images_dir)
    graphs.self_employed_graph(df, output_dir, root_logger, images_dir)
    graphs.correlation_matrix_graph(output_dir, corr_matrix, root_logger, images_dir)
    graphs.total_income_graph(df, output_dir, root_logger, images_dir)
    graphs.chi_square_graph(df, output_dir, root_logger, images_dir)
    graphs.mutual_score_graph(df, output_dir, root_logger, images_dir)

    root_logger.info("=" * 50)
    root_logger.info(f"✅ Усі графіки збережено в папку '{output_dir}/'")
    root_logger.info(f"Створено 12 графіків:")
    root_logger.info("  01_loan_distribution.png")
    root_logger.info("  02_correlation_matrix.png")
    root_logger.info("  03_credit_history.png")
    root_logger.info("  04_marital_status.png")
    root_logger.info("  05_property_area.png")
    root_logger.info("  06_education.png")
    root_logger.info("  07_dependents.png")
    root_logger.info("  08_self_employed.png")
    root_logger.info("  09_correlation_bar.png")
    root_logger.info("  10_income_category.png")
    root_logger.info("  11_chi_square.png")
    root_logger.info("  12_mutual_information.png")
    root_logger.info("=" * 50)
