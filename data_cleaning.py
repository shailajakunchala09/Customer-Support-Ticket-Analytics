"""
data_cleaning.py
-----------------
Reusable data cleaning & preprocessing utilities for the Customer Support
Ticket Analysis project.

Functions in this module are intentionally kept pure (input DataFrame ->
output DataFrame) so they can be unit tested and reused from both the
Jupyter notebook and any future automation/ETL pipeline.
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def load_data(path: str) -> pd.DataFrame:
    """Load the raw ticket CSV file with basic error handling."""
    try:
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} rows from {path}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found at path: {path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error("The provided CSV file is empty.")
        raise


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicated ticket rows (keeps the first occurrence)."""
    before = len(df)
    df = df.drop_duplicates(subset=["Ticket_ID"], keep="first").copy()
    logger.info(f"Removed {before - len(df)} duplicate ticket rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values with business-appropriate strategies:
    - Region: fill with 'Unknown' (categorical, small % missing)
    - Customer_Satisfaction_Rating: leave NaN for unresolved tickets
      (rating genuinely doesn't exist yet); for resolved/closed tickets
      with a missing rating, impute with the median rating of that
      Issue_Category so KPI calculations aren't biased by NaNs.
    - Resolution_Time_Hours: leave NaN for open/in-progress tickets
      (they haven't been resolved yet, so this is not "missing data",
      it is structurally absent).
    """
    df = df.copy()

    df["Region"] = df["Region"].fillna("Unknown")

    resolved_mask = df["Status"].isin(["Resolved", "Closed"])
    median_by_category = (
        df.loc[resolved_mask]
        .groupby("Issue_Category")["Customer_Satisfaction_Rating"]
        .transform("median")
    )
    missing_csat_resolved = resolved_mask & df["Customer_Satisfaction_Rating"].isna()
    df.loc[missing_csat_resolved, "Customer_Satisfaction_Rating"] = median_by_category[missing_csat_resolved]

    logger.info("Missing values handled for Region and Customer_Satisfaction_Rating")
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure correct dtypes for downstream analysis."""
    df = df.copy()
    df["Ticket_Date"] = pd.to_datetime(df["Ticket_Date"], errors="coerce")
    df["Customer_Satisfaction_Rating"] = pd.to_numeric(
        df["Customer_Satisfaction_Rating"], errors="coerce"
    )
    df["Resolution_Time_Hours"] = pd.to_numeric(df["Resolution_Time_Hours"], errors="coerce")
    df["Response_Time_Hours"] = pd.to_numeric(df["Response_Time_Hours"], errors="coerce")

    category_cols = [
        "Issue_Category", "Product_Category", "Priority", "Status",
        "Assigned_Agent", "Region", "Channel", "Escalated"
    ]
    for col in category_cols:
        df[col] = df[col].astype("category")

    logger.info("Data types standardized")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer analysis-friendly derived columns."""
    df = df.copy()
    df["Ticket_Month"] = df["Ticket_Date"].dt.to_period("M").astype(str)
    df["Ticket_Weekday"] = df["Ticket_Date"].dt.day_name()
    df["Is_Resolved"] = df["Status"].isin(["Resolved", "Closed"])

    # SLA target (hours) varies by priority -- a common real-world pattern
    sla_targets = {"Critical": 6, "High": 12, "Medium": 24, "Low": 48}
    df["SLA_Target_Hours"] = df["Priority"].astype(str).map(sla_targets).astype(float)
    df["SLA_Met"] = np.where(
        df["Resolution_Time_Hours"].notna(),
        df["Resolution_Time_Hours"] <= df["SLA_Target_Hours"],
        np.nan
    )
    logger.info("Derived columns added: Ticket_Month, Ticket_Weekday, Is_Resolved, SLA_Target_Hours, SLA_Met")
    return df


def clean_pipeline(path: str) -> pd.DataFrame:
    """Run the full cleaning pipeline end-to-end and return the cleaned df."""
    df = load_data(path)
    df = remove_duplicates(df)
    df["Ticket_Date"] = pd.to_datetime(df["Ticket_Date"], errors="coerce")
    df["Customer_Satisfaction_Rating"] = pd.to_numeric(df["Customer_Satisfaction_Rating"], errors="coerce")
    df["Resolution_Time_Hours"] = pd.to_numeric(df["Resolution_Time_Hours"], errors="coerce")
    df = handle_missing_values(df)
    df = fix_data_types(df)
    df = add_derived_columns(df)
    logger.info(f"Cleaning pipeline complete. Final shape: {df.shape}")
    return df


if __name__ == "__main__":
    cleaned = clean_pipeline("data/customer_support_tickets.csv")
    cleaned.to_csv("data/customer_support_tickets_cleaned.csv", index=False)
    print("Cleaned dataset saved to data/customer_support_tickets_cleaned.csv")
    print(cleaned.info())
