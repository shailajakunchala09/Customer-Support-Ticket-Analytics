"""
visualization.py
-----------------
Generates the core EDA charts for the Customer Support Ticket Analysis
project and saves them as PNG files under screenshots/ so they can be
embedded directly in the README and the project report.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

from data_cleaning import clean_pipeline
import kpi_analysis as kpi

plt.rcParams["figure.dpi"] = 110
COLOR_PRIMARY = "#2E86AB"
COLOR_ACCENT = "#F24236"
COLOR_PALETTE = ["#2E86AB", "#F6AE2D", "#F24236", "#33A1A1", "#7B4B94", "#5C946E"]

OUT_DIR = "screenshots"


def save(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def plot_monthly_trend(df):
    trend = kpi.monthly_ticket_trend(df)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(trend.index, trend.values, marker="o", color=COLOR_PRIMARY, linewidth=2)
    ax.fill_between(range(len(trend)), trend.values, alpha=0.15, color=COLOR_PRIMARY)
    ax.set_title("Monthly Ticket Volume Trend (2024)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Tickets")
    plt.xticks(rotation=45)
    ax.grid(alpha=0.3)
    save(fig, "01_monthly_ticket_trend.png")


def plot_issue_category_distribution(df):
    counts = df["Issue_Category"].value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(counts.index[::-1], counts.values[::-1], color=COLOR_PRIMARY)
    ax.set_title("Ticket Volume by Issue Category", fontsize=13, fontweight="bold")
    ax.set_xlabel("Number of Tickets")
    save(fig, "02_issue_category_distribution.png")


def plot_priority_distribution(df):
    counts = df["Priority"].value_counts().reindex(["Low", "Medium", "High", "Critical"])
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=COLOR_PALETTE,
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Ticket Priority Distribution", fontsize=13, fontweight="bold")
    save(fig, "03_priority_distribution.png")


def plot_status_distribution(df):
    counts = df["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(counts.index, counts.values, color=COLOR_PALETTE)
    ax.set_title("Ticket Status Breakdown", fontsize=13, fontweight="bold")
    ax.set_ylabel("Number of Tickets")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 20, str(int(b.get_height())),
                ha="center", fontsize=9)
    save(fig, "04_status_distribution.png")


def plot_resolution_time_by_priority(df):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    data = [df[df["Priority"] == p]["Resolution_Time_Hours"].dropna() for p in ["Low", "Medium", "High", "Critical"]]
    box = ax.boxplot(data, labels=["Low", "Medium", "High", "Critical"], patch_artist=True, showfliers=False)
    for patch, color in zip(box["boxes"], COLOR_PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title("Resolution Time (Hours) by Priority", fontsize=13, fontweight="bold")
    ax.set_ylabel("Resolution Time (Hours)")
    save(fig, "05_resolution_time_by_priority.png")


def plot_regional_csat(df):
    reg = kpi.regional_csat(df)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(reg.index, reg.values, color=COLOR_PRIMARY)
    ax.set_title("Average Customer Satisfaction by Region", fontsize=13, fontweight="bold")
    ax.set_ylabel("Avg CSAT (1-5)")
    ax.set_ylim(0, 5)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.05, f"{b.get_height():.2f}",
                ha="center", fontsize=9)
    save(fig, "06_regional_csat.png")


def plot_agent_performance(df):
    perf = kpi.agent_performance(df).sort_values("Avg_CSAT", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(perf.index, perf["Avg_CSAT"], color=COLOR_PRIMARY)
    ax.set_title("Agent Performance: Average CSAT by Agent", fontsize=13, fontweight="bold")
    ax.set_xlabel("Average CSAT (1-5)")
    ax.set_xlim(0, 5)
    save(fig, "07_agent_performance_csat.png")


def plot_channel_distribution(df):
    counts = df["Channel"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=COLOR_PALETTE,
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Tickets by Support Channel", fontsize=13, fontweight="bold")
    save(fig, "08_channel_distribution.png")


def plot_sla_compliance(df):
    sla = df["SLA_Met"].dropna()
    met_pct = sla.mean() * 100
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([met_pct, 100 - met_pct], labels=["SLA Met", "SLA Breached"],
           autopct="%1.1f%%", colors=[COLOR_PRIMARY, COLOR_ACCENT],
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Overall SLA Compliance", fontsize=13, fontweight="bold")
    save(fig, "09_sla_compliance.png")


def plot_escalation_by_priority(df):
    esc = df.groupby("Priority", observed=True)["Escalated"].apply(lambda x: (x == "Yes").mean() * 100)
    esc = esc.reindex(["Low", "Medium", "High", "Critical"])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(esc.index, esc.values, color=COLOR_ACCENT)
    ax.set_title("Escalation Rate (%) by Priority", fontsize=13, fontweight="bold")
    ax.set_ylabel("Escalation Rate (%)")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"{b.get_height():.1f}%",
                ha="center", fontsize=9)
    save(fig, "10_escalation_by_priority.png")


def generate_all_charts(df):
    plot_monthly_trend(df)
    plot_issue_category_distribution(df)
    plot_priority_distribution(df)
    plot_status_distribution(df)
    plot_resolution_time_by_priority(df)
    plot_regional_csat(df)
    plot_agent_performance(df)
    plot_channel_distribution(df)
    plot_sla_compliance(df)
    plot_escalation_by_priority(df)


if __name__ == "__main__":
    df = clean_pipeline("data/customer_support_tickets.csv")
    generate_all_charts(df)
    print("\nAll EDA charts generated in the 'screenshots/' folder.")
