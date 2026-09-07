"""
kpi_analysis.py
----------------
Business KPI calculations for the Customer Support Ticket Analysis project.

Each function returns a small, print/dashboard-friendly result (scalar,
Series, or DataFrame) so it can be reused directly inside the notebook,
a script, or wired into a future dashboard/API layer.
"""

import pandas as pd
import numpy as np


def total_tickets(df: pd.DataFrame) -> int:
    return len(df)


def status_breakdown(df: pd.DataFrame) -> pd.Series:
    return df["Status"].value_counts()


def avg_resolution_time(df: pd.DataFrame) -> float:
    return round(df["Resolution_Time_Hours"].mean(), 2)


def avg_response_time(df: pd.DataFrame) -> float:
    return round(df["Response_Time_Hours"].mean(), 2)


def avg_csat(df: pd.DataFrame) -> float:
    return round(df["Customer_Satisfaction_Rating"].mean(), 2)


def sla_compliance_rate(df: pd.DataFrame) -> float:
    """% of resolved tickets that met their priority-based SLA target."""
    resolved = df[df["SLA_Met"].notna()]
    if len(resolved) == 0:
        return 0.0
    return round(resolved["SLA_Met"].mean() * 100, 2)


def escalation_rate(df: pd.DataFrame) -> float:
    return round((df["Escalated"] == "Yes").mean() * 100, 2)


def top_issue_categories(df: pd.DataFrame, n: int = 5) -> pd.Series:
    return df["Issue_Category"].value_counts().head(n)


def category_wise_resolution_time(df: pd.DataFrame) -> pd.Series:
    return df.groupby("Issue_Category", observed=True)["Resolution_Time_Hours"].mean().sort_values(ascending=False)


def agent_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an agent performance scorecard: tickets handled, average
    resolution time, average CSAT, and SLA compliance rate.
    """
    perf = df.groupby("Assigned_Agent", observed=True).agg(
        Tickets_Handled=("Ticket_ID", "count"),
        Avg_Resolution_Time=("Resolution_Time_Hours", "mean"),
        Avg_CSAT=("Customer_Satisfaction_Rating", "mean"),
        SLA_Compliance_Pct=("SLA_Met", "mean"),
        Escalation_Rate_Pct=("Escalated", lambda x: (x == "Yes").mean() * 100),
    ).round(2)
    perf["SLA_Compliance_Pct"] = (perf["SLA_Compliance_Pct"] * 100).round(2)
    return perf.sort_values("Avg_CSAT", ascending=False)


def monthly_ticket_trend(df: pd.DataFrame) -> pd.Series:
    return df.groupby("Ticket_Month", observed=True)["Ticket_ID"].count().sort_index()


def regional_csat(df: pd.DataFrame) -> pd.Series:
    return df.groupby("Region", observed=True)["Customer_Satisfaction_Rating"].mean().round(2).sort_values(ascending=False)


def priority_distribution(df: pd.DataFrame) -> pd.Series:
    return df["Priority"].value_counts()


def high_priority_unresolved(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        (df["Priority"].isin(["High", "Critical"])) &
        (~df["Status"].isin(["Resolved", "Closed"]))
    ][["Ticket_ID", "Priority", "Status", "Assigned_Agent", "Ticket_Date"]]


def channel_distribution(df: pd.DataFrame) -> pd.Series:
    return df["Channel"].value_counts()


def generate_kpi_summary(df: pd.DataFrame) -> dict:
    """Single dict of headline KPIs -- handy for a dashboard summary card."""
    return {
        "Total Tickets": total_tickets(df),
        "Open Tickets": int((df["Status"] == "Open").sum()),
        "In Progress Tickets": int((df["Status"] == "In Progress").sum()),
        "Resolved Tickets": int((df["Status"] == "Resolved").sum()),
        "Closed Tickets": int((df["Status"] == "Closed").sum()),
        "Avg Resolution Time (Hrs)": avg_resolution_time(df),
        "Avg Response Time (Hrs)": avg_response_time(df),
        "Avg CSAT (1-5)": avg_csat(df),
        "SLA Compliance (%)": sla_compliance_rate(df),
        "Escalation Rate (%)": escalation_rate(df),
    }


if __name__ == "__main__":
    from data_cleaning import clean_pipeline

    df = clean_pipeline("data/customer_support_tickets.csv")
    summary = generate_kpi_summary(df)
    print("\n=== KPI SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {v}")

    print("\n=== TOP 5 ISSUE CATEGORIES ===")
    print(top_issue_categories(df))

    print("\n=== AGENT PERFORMANCE (Top 5 by CSAT) ===")
    print(agent_performance(df).head())
