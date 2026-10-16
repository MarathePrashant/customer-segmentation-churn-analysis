# CUSTOMER SHOPPING BEHAVIOR ANALYSIS
# Data Cleaning, Feature Engineering, Business Analysis & ETL


import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd

# PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Look for the dataset in the data folder first,
# then in the main project folder.
possible_input_paths = [
    DATA_DIR / "customer_shopping_behavior.csv",
    BASE_DIR / "customer_shopping_behavior.csv",
]

INPUT_FILE = next(
    (file_path for file_path in possible_input_paths if file_path.exists()),
    None
)

CLEANED_FILE = OUTPUT_DIR / "customer_shopping_behavior_cleaned.csv"
DATA_QUALITY_FILE = OUTPUT_DIR / "data_quality_report.csv"
CATEGORY_SUMMARY_FILE = OUTPUT_DIR / "category_analysis.csv"
AGE_GROUP_SUMMARY_FILE = OUTPUT_DIR / "age_group_analysis.csv"


# LOGGING

logging.basicConfig(
    filename=LOG_DIR / "customer_shopping_behavior.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)

logging.info("Starting Customer Shopping Behavior ETL pipeline.")


# LOAD DATA

if INPUT_FILE is None:
    error_message = (
        "Dataset not found. Place 'customer_shopping_behavior.csv' "
        "inside the project folder or its 'data' folder."
    )
    logging.error(error_message)
    raise FileNotFoundError(error_message)

print("\n" + "=" * 60)
print("CUSTOMER SHOPPING BEHAVIOR ANALYSIS")
print("=" * 60)

print(f"\nReading dataset from:\n{INPUT_FILE}")
logging.info("Reading source file: %s", INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully.")
print(f"Total records: {df.shape[0]:,}")
print(f"Total columns: {df.shape[1]}")

logging.info(
    "Dataset loaded successfully. Rows: %s | Columns: %s",
    df.shape[0],
    df.shape[1]
)


# INITIAL DATA EXPLORATION

print("\nFirst Five Rows:")
print(df.head())

print("\nLast Five Rows:")
print(df.tail())

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe(include="all").T)

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())


# STANDARDIZE COLUMN NAMES

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

df = df.rename(
    columns={
        "purchase_amount_usd": "purchase_amount"
    }
)

print("\nStandardized Column Names:")
print(df.columns.tolist())


# DATA VALIDATION

required_columns = [
    "customer_id",
    "age",
    "category",
    "purchase_amount",
    "review_rating",
    "frequency_of_purchases",
    "discount_applied",
    "promo_code_used",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    error_message = f"Required columns are missing: {missing_columns}"
    logging.error(error_message)
    raise ValueError(error_message)

# Convert calculation fields to numeric values.
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["purchase_amount"] = pd.to_numeric(
    df["purchase_amount"], errors="coerce"
)
df["review_rating"] = pd.to_numeric(
    df["review_rating"], errors="coerce"
)

print("\nMissing or Invalid Numeric Values:")
print(
    df[["age", "purchase_amount", "review_rating"]]
    .isnull()
    .sum()
)


# HANDLE MISSING REVIEW RATINGS

# Fill missing ratings with the median rating of their category.
# If a category has no available median, use the overall median.

if df["review_rating"].isnull().any():

    overall_rating_median = df["review_rating"].median()

    category_rating_median = df.groupby(
        "category"
    )["review_rating"].transform("median")

    df["review_rating"] = df["review_rating"].fillna(
        category_rating_median
    )

    df["review_rating"] = df["review_rating"].fillna(
        overall_rating_median
    )

remaining_rating_missing = df["review_rating"].isnull().sum()

if remaining_rating_missing > 0:
    logging.warning(
        "%s review ratings remain missing because no valid median was available.",
        remaining_rating_missing
    )

print("\nMissing Values After Review Rating Treatment:")
print(df.isnull().sum())


# REMOVE DUPLICATE RECORDS


duplicate_count = df.duplicated().sum()

print(f"\nDuplicate Rows Found: {duplicate_count:,}")

if duplicate_count > 0:
    df = df.drop_duplicates().copy()
    print(f"Duplicate rows removed: {duplicate_count:,}")
else:
    print("No duplicate rows found.")

df = df.reset_index(drop=True)

print("\nDataset Shape After Removing Duplicates:")
print(df.shape)


# FEATURE ENGINEERING: AGE GROUP

age_bins = [0, 25, 35, 50, np.inf]

age_labels = [
    "Young Adult",
    "Adult",
    "Middle Age",
    "Senior"
]

df["age_group"] = pd.cut(
    df["age"],
    bins=age_bins,
    labels=age_labels,
    right=False
)

print("\nAge Group Preview:")
print(df[["age", "age_group"]].head(10))

print("\nAge Group Analysis:")

age_group_summary = (
    df.groupby("age_group", observed=False)
    .agg(
        customer_records=("customer_id", "count")
    )
    .reset_index()
)

age_group_summary["percentage_of_records"] = (
    age_group_summary["customer_records"]
    / max(len(df), 1)
    * 100
).round(2)

print(age_group_summary)


# FEATURE ENGINEERING: PURCHASE FREQUENCY

# Map each purchase frequency to its approximate number of days.
# Bi-Weekly and Fortnightly are both represented as 14 days.
# Quarterly and Every 3 Months are both represented as 90 days.

frequency_map = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90,
}

df["frequency_of_purchases"] = (
    df["frequency_of_purchases"]
    .astype("string")
    .str.strip()
)

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"]
    .map(frequency_map)
    .astype("Int64")
)

print("\nPurchase Frequency Analysis:")
print(
    df[
        ["frequency_of_purchases", "purchase_frequency_days"]
    ].head(10)
)

print("\nUnmapped Purchase Frequency Values:")

unmapped_frequencies = df.loc[
    df["purchase_frequency_days"].isna(),
    "frequency_of_purchases"
].value_counts(dropna=False)

if unmapped_frequencies.empty:
    print("None. All purchase frequency values were mapped.")
else:
    print(unmapped_frequencies)

    logging.warning(
        "Unmapped purchase frequency values found: %s",
        unmapped_frequencies.to_dict()
    )


# CHECK DISCOUNT AND PROMO CODE FIELDS

print("\nDiscount and Promo Code Comparison:")
print(df[["discount_applied", "promo_code_used"]].head(10))

columns_are_identical = df["discount_applied"].equals(
    df["promo_code_used"]
)

print(f"\nAre Both Columns Identical? {columns_are_identical}")

# Remove the promo column only when its values exactly match
# the discount column. Otherwise, retain both columns.

if columns_are_identical:
    df = df.drop(columns=["promo_code_used"])

    print(
        "\nPromo Code Used was removed because it exactly "
        "duplicates Discount Applied."
    )
else:
    print(
        "\nBoth columns were retained because their values differ."
    )

# BUSINESS ANALYSIS: CATEGORY PERFORMANCE

category_summary = (
    df.groupby("category", dropna=False)
    .agg(
        customer_records=("customer_id", "count"),
        total_purchase_amount=("purchase_amount", "sum"),
        average_purchase_amount=("purchase_amount", "mean"),
        median_purchase_amount=("purchase_amount", "median"),
        average_review_rating=("review_rating", "mean"),
    )
    .reset_index()
)

category_summary["average_purchase_amount"] = (
    category_summary["average_purchase_amount"].round(2)
)

category_summary["median_purchase_amount"] = (
    category_summary["median_purchase_amount"].round(2)
)

category_summary["average_review_rating"] = (
    category_summary["average_review_rating"].round(2)
)

category_summary = category_summary.sort_values(
    by="total_purchase_amount",
    ascending=False
)

print("\nCategory-Wise Analysis:")
print(category_summary)

# BUSINESS ANALYSIS: OVERALL SHOPPING METRICS

total_purchase_amount = df["purchase_amount"].sum()

average_purchase_amount = df["purchase_amount"].mean()

average_review_rating = df["review_rating"].mean()

unique_customers = df["customer_id"].nunique()

print("\nOverall Business Metrics:")
print(f"Customer records: {len(df):,}")
print(f"Unique customer IDs: {unique_customers:,}")
print(f"Total purchase amount: ${total_purchase_amount:,.2f}")
print(f"Average purchase amount: ${average_purchase_amount:,.2f}")
print(f"Average review rating: {average_review_rating:.2f} / 5")


# DATA QUALITY REPORT

data_quality_report = pd.DataFrame({
    "column": df.columns,
    "data_type": [
        str(df[column].dtype) for column in df.columns
    ],
    "missing_values": [
        df[column].isnull().sum() for column in df.columns
    ],
    "unique_values": [
        df[column].nunique(dropna=True) for column in df.columns
    ],
})

data_quality_report["missing_percentage"] = (
    data_quality_report["missing_values"]
    / max(len(df), 1)
    * 100
).round(2)

data_quality_report = data_quality_report[
    [
        "column",
        "data_type",
        "missing_values",
        "missing_percentage",
        "unique_values",
    ]
]

print("\nData Quality Report:")
print(data_quality_report.to_string(index=False))


# FINAL DATA VALIDATION

print("\nFinal Missing Values:")
print(df.isnull().sum())

print(f"\nFinal Dataset Shape: {df.shape}")

if df["purchase_frequency_days"].isnull().any():
    logging.warning(
        "Final validation found unmapped purchase frequencies."
    )
else:
    logging.info(
        "All purchase frequency values were successfully mapped."
    )


# EXPORT CLEANED DATA AND REPORTS

df.to_csv(CLEANED_FILE, index=False)

data_quality_report.to_csv(
    DATA_QUALITY_FILE,
    index=False
)

category_summary.to_csv(
    CATEGORY_SUMMARY_FILE,
    index=False
)

age_group_summary.to_csv(
    AGE_GROUP_SUMMARY_FILE,
    index=False
)

print("\nCleaned Dataset Saved Successfully!")
print(f"Cleaned dataset: {CLEANED_FILE}")
print(f"Data quality report: {DATA_QUALITY_FILE}")
print(f"Category analysis: {CATEGORY_SUMMARY_FILE}")
print(f"Age group analysis: {AGE_GROUP_SUMMARY_FILE}")

logging.info("Cleaned dataset exported to %s", CLEANED_FILE)
logging.info("Data quality report exported to %s", DATA_QUALITY_FILE)
logging.info("Category analysis exported to %s", CATEGORY_SUMMARY_FILE)
logging.info("Age group analysis exported to %s", AGE_GROUP_SUMMARY_FILE)


# OPTIONAL: LOAD DATA INTO POSTGRESQL


# Configure these environment variables before enabling loading:
#
# LOAD_TO_POSTGRES=true
# PGHOST=loca---------host
# PGPORT=####
# PGDATABASE=shopping_behavior
# PGUSER=postgres
# PGPASSWORD=your_password
#
# Install required packages if needed:
# pip install sqlalchemy psycopg2-binary

load_to_postgres = (
    os.getenv("LOAD_TO_POSTGRES", "false").strip().lower() == "true"
)

if load_to_postgres:

    try:
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL

        pg_host = os.getenv("PGHOST", "localhost")
        pg_port = int(os.getenv("PGPORT", "5432"))
        pg_database = os.getenv("PGDATABASE", "shopping_behavior")
        pg_user = os.getenv("PGUSER", "postgres")
        pg_password = os.getenv("PGPASSWORD")

        if not pg_password:
            raise ValueError(
                "PGPASSWORD is not set. Configure it as an "
                "environment variable before enabling PostgreSQL loading."
            )

        database_url = URL.create(
            drivername="postgresql+psycopg2",
            username=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            database=pg_database,
        )

        engine = create_engine(database_url)

        df.to_sql(
            "customer_behavior",
            engine,
            if_exists="replace",
            index=False
        )

        print(
            "\nData successfully loaded into PostgreSQL table "
            "'customer_behavior'."
        )

        logging.info("Data successfully loaded into PostgreSQL.")

        engine.dispose()

    except Exception:
        logging.exception("PostgreSQL loading failed.")
        raise

else:
    print(
        "\nPostgreSQL loading skipped. Set LOAD_TO_POSTGRES=true "
        "and configure the PG environment variables to enable it."
    )

# PIPELINE SUMMARY

print("\n" + "=" * 60)
print("CUSTOMER SHOPPING BEHAVIOR ETL PIPELINE COMPLETED")
print("=" * 60)

print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns):,}")

print(
    "Unmapped purchase frequencies: "
    f"{df['purchase_frequency_days'].isna().sum():,}"
)

print(f"Output directory: {OUTPUT_DIR}")

logging.info(
    "ETL pipeline completed. Rows: %s | Columns: %s",
    df.shape[0],
    df.shape[1]
)
