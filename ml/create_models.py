import os

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "loan_data.csv")

# ЗАВАНТАЖЕННЯ ДАНИХ
df = pd.read_csv(csv_path)


# ОБРОБКА ПРОПУЩЕНИХ ЗНАЧЕНЬ
categorical_columns = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "Property_Area",
]

for col in categorical_columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)

numerical_columns = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
]

for col in numerical_columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)


# ПОПЕРЕДНЯ ОБРОБКА ОЗНАК
df["Dependents"] = df["Dependents"].replace("3+", "3")
df["Dependents"] = df["Dependents"].astype(int)
df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

# РОЗДІЛЕННЯ НА ОЗНАКИ ТА ЦІЛЬОВУ ЗМІННУ
X = df.drop(["Loan_ID", "Loan_Status"], axis=1)
y = df["Loan_Status"]

# ПІДГОТОВКА ДВОХ ВАРІАНТІВ ДАНИХ
print("\n" + "=" * 60)
print("ПІДГОТОВКА ДВОХ ВАРІАНТІВ МОДЕЛЕЙ")
print("=" * 60)

# Варіант 1: З Credit_History
categorical_features_with = [
    "Gender",
    "Married",
    "Education",
    "Self_Employed",
    "Property_Area",
]
numerical_features_with = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Dependents",
    "Credit_History",
]

# Створення препроцесорів
preprocessor_with = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features_with),
        (
            "cat",
            OneHotEncoder(drop="first", sparse_output=False),
            categorical_features_with,
        ),
    ]
)

# РОЗДІЛЕННЯ НА TRAIN/TEST
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# СТВОРЕННЯ ТА НАВЧАННЯ МОДЕЛЕЙ
print("\n" + "=" * 60)
print("НАВЧАННЯ МОДЕЛЕЙ З ОПТИМІЗАЦІЄЮ ГІПЕРПАРАМЕТРІВ")
print("=" * 60)

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import time

# МОДЕЛІ З CREDIT_HISTORY
print("\n---- МОДЕЛІ З CREDIT_HISTORY")
print("-" * 60)

# Pipelines
pipeline_rf_with = Pipeline(
    [
        ("preprocessor", preprocessor_with),
        ("classifier", RandomForestClassifier(random_state=42)),
    ]
)

pipeline_lr_with = Pipeline(
    [
        ("preprocessor", preprocessor_with),
        ("classifier", LogisticRegression(random_state=42, max_iter=1000)),
    ]
)

pipeline_gb_with = Pipeline(
    [
        ("preprocessor", preprocessor_with),
        ("classifier", GradientBoostingClassifier(random_state=42)),
    ]
)

pipeline_svm_with = Pipeline(
    [
        ("preprocessor", preprocessor_with),
        ("classifier", SVC(random_state=42, probability=True)),
    ]
)


# Параметри для Grid Search
rf_params = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [5, 10, None],
    "classifier__min_samples_split": [2, 5],
    "classifier__min_samples_leaf": [1, 2],
}

lr_params = {
    "classifier__C": [0.1, 1, 10, 100],
    "classifier__solver": ["liblinear", "lbfgs"],
    "classifier__penalty": ["l2"],
}

gb_params = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__learning_rate": [0.05, 0.1, 0.2],
    "classifier__max_depth": [3, 5, 7],
}

svm_params = {
    "classifier__C": [0.1, 1, 10],
    "classifier__kernel": ["rbf", "linear"],
    "classifier__gamma": ["scale", "auto"],
}

# Об'єднання моделей для навчання
models_info = [
    ("RF з Credit_History", pipeline_rf_with, rf_params),
    ("LR з Credit_History", pipeline_lr_with, lr_params),
    ("GB з Credit_History", pipeline_gb_with, gb_params),
    ("SVM з Credit_History", pipeline_svm_with, svm_params),
]

best_models = {}
results_summary = []

print("\nЗапуск Grid Search для всіх моделей...")
print("   (це може зайняти кілька хвилин...)\n")

for name, pipeline, params in models_info:
    print(f"   Оптимізація {name}...")
    start_time = time.time()

    grid_search = GridSearchCV(
        pipeline, params, cv=5, scoring="accuracy", n_jobs=-1, verbose=0
    )

    grid_search.fit(X_train, y_train)
    best_models[name] = grid_search.best_estimator_

    test_score = grid_search.score(X_test, y_test)
    train_score = grid_search.score(X_train, y_train)
    cv_scores = cross_val_score(grid_search.best_estimator_, X_train, y_train, cv=5)

    elapsed_time = time.time() - start_time

    results_summary.append(
        {
            "Model": name,
            "Best_Params": grid_search.best_params_,
            "CV_Score": grid_search.best_score_,
            "Train_Score": train_score,
            "Test_Score": test_score,
            "CV_Mean": cv_scores.mean(),
            "CV_Std": cv_scores.std(),
            "Time": elapsed_time,
        }
    )

    print(f"   ✓ Завершено за {elapsed_time:.1f}с")

# ПОПЕРЕДНЯ ОБРОБКА ОЗНАК
df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
df["Income_to_Loan"] = df["Total_Income"] / (df["LoanAmount"] + 1)
df["Loan_per_Term"] = df["LoanAmount"] / (df["Loan_Amount_Term"] + 1)
df["Is_Graduate_and_Employed"] = np.where(
    (df["Education"] == "Graduate") & (df["Self_Employed"] == "No"), 1, 0
)

# Варіант 2: Без Credit_History
categorical_features_without = [
    "Gender",
    "Married",
    "Education",
    "Self_Employed",
    "Property_Area",
]
numerical_features_without = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Dependents",
    "Total_Income",
    "Income_to_Loan",
    "Loan_per_Term",
    "Is_Graduate_and_Employed",
]

# РОЗДІЛЕННЯ НА ОЗНАКИ ТА ЦІЛЬОВУ ЗМІННУ
X = df.drop(["Loan_ID", "Loan_Status"], axis=1)
y = df["Loan_Status"]


X_without = X.drop("Credit_History", axis=1)

# Створення препроцесорів
preprocessor_without = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features_without),
        (
            "cat",
            OneHotEncoder(drop="first", sparse_output=False),
            categorical_features_without,
        ),
    ]
)

# РОЗДІЛЕННЯ НА TRAIN/TEST
X_train_without, X_test_without, _, _ = train_test_split(
    X_without, y, test_size=0.2, random_state=42, stratify=y
)

# МОДЕЛІ БЕЗ CREDIT_HISTORY
print("\n---- МОДЕЛІ БЕЗ CREDIT_HISTORY")
print("-" * 60)

# Pipelines
pipeline_rf_without = Pipeline(
    [
        ("preprocessor", preprocessor_without),
        (
            "classifier",
            RandomForestClassifier(random_state=42, class_weight="balanced"),
        ),
    ]
)

pipeline_lr_without = Pipeline(
    [
        ("preprocessor", preprocessor_without),
        (
            "classifier",
            LogisticRegression(random_state=42, max_iter=1000, class_weight="balanced"),
        ),
    ]
)

pipeline_gb_without = Pipeline(
    [
        ("preprocessor", preprocessor_without),
        ("classifier", GradientBoostingClassifier(random_state=42)),
    ]
)

pipeline_svm_without = Pipeline(
    [
        ("preprocessor", preprocessor_without),
        ("classifier", SVC(random_state=42, probability=True)),
    ]
)

# Об'єднання моделей для навчання
models_info = [
    ("RF без Credit_History", pipeline_rf_without, rf_params),
    ("LR без Credit_History", pipeline_lr_without, lr_params),
    ("GB без Credit_History", pipeline_gb_without, gb_params),
    ("SVM без Credit_History", pipeline_svm_without, svm_params),
]

print("\nЗапуск Grid Search для всіх моделей...")
print("   (це може зайняти кілька хвилин...)\n")

for name, pipeline, params in models_info:
    print(f"   Оптимізація {name}...")
    start_time = time.time()

    grid_search = GridSearchCV(
        pipeline, params, cv=5, scoring="roc_auc", n_jobs=-1, verbose=0
    )

    grid_search.fit(X_train_without, y_train)
    best_models[name] = grid_search.best_estimator_

    test_score = grid_search.score(X_test_without, y_test)
    train_score = grid_search.score(X_train_without, y_train)
    cv_scores = cross_val_score(
        grid_search.best_estimator_, X_train_without, y_train, cv=5
    )

    elapsed_time = time.time() - start_time

    results_summary.append(
        {
            "Model": name,
            "Best_Params": grid_search.best_params_,
            "CV_Score": grid_search.best_score_,
            "Train_Score": train_score,
            "Test_Score": test_score,
            "CV_Mean": cv_scores.mean(),
            "CV_Std": cv_scores.std(),
            "Time": elapsed_time,
        }
    )

    print(f"   ✓ Завершено за {elapsed_time:.1f}с")

# ПОРІВНЯННЯ РЕЗУЛЬТАТІВ
print("\n" + "=" * 80)
print("ПОРІВНЯННЯ ВСІХ МОДЕЛЕЙ")
print("=" * 80)

results_df = pd.DataFrame(results_summary)
results_df_sorted = results_df.sort_values("Test_Score", ascending=False)

print(
    f"{'Модель':<30} {'CV Score':<10} {'Train':<8} {'Test':<8} {'CV±Std':<12} {'Час':<8}"
)
print("-" * 90)

for _, row in results_df_sorted.iterrows():
    cv_std_str = f"{row['CV_Mean']:.3f}±{row['CV_Std']:.3f}"
    print(
        f"{row['Model']:<30} {row['CV_Score']:<10.4f} {row['Train_Score']:<8.4f} "
        f"{row['Test_Score']:<8.4f} {cv_std_str:<12} {row['Time']:<8.1f}s"
    )

# Порівняння моделей З та БЕЗ Credit_History
print("\n" + "=" * 80)
print("ВПЛИВ CREDIT_HISTORY НА ТОЧНІСТЬ")
print("=" * 80)

for model_type in ["RF", "LR", "GB", "SVM"]:
    with_ch = results_df[results_df["Model"] == f"{model_type} з Credit_History"][
        "Test_Score"
    ].values
    without_ch = results_df[results_df["Model"] == f"{model_type} без Credit_History"][
        "Test_Score"
    ].values

    if len(with_ch) > 0 and len(without_ch) > 0:
        diff = with_ch[0] - without_ch[0]
        diff_percent = diff * 100
        print(
            f"{model_type:3s}: З CH: {with_ch[0]:.4f} | Без CH: {without_ch[0]:.4f} | "
            f"Різниця: {diff:+.4f} ({diff_percent:+.2f}%)"
        )

# НАЙКРАЩІ МОДЕЛІ
best_with_ch = (
    results_df[results_df["Model"].str.contains("з Credit_History")]
    .sort_values("Test_Score", ascending=False)
    .iloc[0]
)
best_without_ch = (
    results_df[results_df["Model"].str.contains("без Credit_History")]
    .sort_values("Test_Score", ascending=False)
    .iloc[0]
)

print("\n" + "=" * 80)
print("НАЙКРАЩІ МОДЕЛІ")
print("=" * 80)

print(f"\n Найкраща модель З Credit_History:")
print(f"   Модель: {best_with_ch['Model']}")
print(f"   Test Score: {best_with_ch['Test_Score']:.4f}")
print(f"   Параметри: {best_with_ch['Best_Params']}")

print(f"\n Найкраща модель БЕЗ Credit_History:")
print(f"   Модель: {best_without_ch['Model']}")
print(f"   Test Score: {best_without_ch['Test_Score']:.4f}")
print(f"   Параметри: {best_without_ch['Best_Params']}")

# ЗБЕРЕЖЕННЯ МОДЕЛЕЙ
print("\n" + "=" * 80)
print("ЗБЕРЕЖЕННЯ МОДЕЛЕЙ")
print("=" * 80)

best_model_with = best_models[best_with_ch["Model"]]
best_model_without = best_models[best_without_ch["Model"]]


models_dir = os.path.join(os.path.dirname(__file__), "../ml_data")
os.makedirs(models_dir, exist_ok=True)

# Шляхи до файлів
model_with_path = os.path.join(models_dir, "best_model_with_credit_history.pkl")
model_without_path = os.path.join(models_dir, "best_model_without_credit_history.pkl")

# Збереження
joblib.dump(best_model_with, model_with_path)
joblib.dump(best_model_without, model_without_path)

print(f"Моделі збережені в: {models_dir}")


print("Збережені файли:")
print("   • best_model_with_credit_history.pkl")
print("   • best_model_without_credit_history.pkl")

print(f"\nНавчання завершено!")
print(f"   Загальний час: {sum(r['Time'] for r in results_summary):.1f} секунд")
print(
    f"   Різниця в точності: {(best_with_ch['Test_Score'] - best_without_ch['Test_Score'])*100:+.2f}%"
)
