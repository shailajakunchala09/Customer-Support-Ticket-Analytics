"""
generate_dataset.py
--------------------
Generates a realistic, synthetic Customer Support Ticket dataset for the
Customer Support Ticket Analysis project.

The dataset simulates 12 months of support ticket activity for a mid-size
company handling tickets across multiple products, regions and channels.
Realistic correlations are built in on purpose (e.g. Critical priority
tickets take longer to resolve and get lower CSAT when resolution time is
high; Phone channel tickets resolve faster than Email; certain agents
perform better than others) so that the analysis notebook has genuine
patterns to discover instead of pure random noise.

Run:
    python src/generate_dataset.py

Output:
    data/customer_support_tickets.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# ----------------------------------------------------------------------
# Reproducibility
# ----------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

N_RECORDS = 12000  # slightly above the required 10,000 to allow for
                    # cleaning/deduplication demos without dropping below 10k

# ----------------------------------------------------------------------
# Reference / lookup data
# ----------------------------------------------------------------------
ISSUE_CATEGORIES = [
    "Billing Issue", "Login Problem", "Product Defect", "Delivery Delay",
    "Refund Request", "Technical Support", "Account Access", "Payment Failure",
    "Order Cancellation", "Warranty Claim", "Feature Request", "App Crash"
]

PRODUCT_CATEGORIES = [
    "Electronics", "Home Appliances", "Mobile & Accessories", "Fashion",
    "Software/Subscription", "Groceries", "Furniture", "Books & Media"
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [0.35, 0.35, 0.20, 0.10]

STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

REGIONS = ["North", "South", "East", "West", "Central"]

CHANNELS = ["Email", "Chat", "Phone", "Web"]
CHANNEL_WEIGHTS = [0.30, 0.28, 0.22, 0.20]

AGENTS = [
    "Aarav Sharma", "Priya Nair", "Rohan Mehta", "Ishita Kapoor", "Karan Verma",
    "Sneha Reddy", "Aditya Singh", "Neha Gupta", "Vikram Rao", "Ananya Iyer",
    "Rahul Joshi", "Divya Menon", "Arjun Malhotra", "Pooja Desai", "Manish Kumar"
]

# Give each agent a hidden "skill factor" that influences resolution speed
# and CSAT -- this creates realistic performance spread for the
# agent-performance analysis section.
AGENT_SKILL = {agent: np.random.uniform(0.75, 1.25) for agent in AGENTS}

ESCALATED_OPTIONS = ["Yes", "No"]


def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def generate_dataset(n=N_RECORDS):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31, 23, 59, 59)

    records = []

    for i in range(1, n + 1):
        ticket_id = f"TCK{100000 + i}"
        customer_id = f"CUST{random.randint(10000, 49999)}"
        ticket_date = random_date(start_date, end_date)

        issue_category = random.choice(ISSUE_CATEGORIES)
        product_category = random.choice(PRODUCT_CATEGORIES)
        priority = np.random.choice(PRIORITIES, p=PRIORITY_WEIGHTS)
        channel = np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS)
        region = random.choice(REGIONS)
        agent = random.choice(AGENTS)
        skill = AGENT_SKILL[agent]

        # ---- Response time (hours) ----------------------------------
        # Faster channels: Chat/Phone respond quicker than Email/Web
        base_response = {"Chat": 1.0, "Phone": 0.5, "Email": 4.0, "Web": 3.0}[channel]
        response_time = max(0.1, np.random.exponential(base_response) / skill)

        # ---- Resolution time (hours) ---------------------------------
        # Higher priority tickets are worked faster in relative terms,
        # but Critical/High issues are often technically harder, so the
        # base resolution time still trends up with severity.
        priority_base = {"Low": 20, "Medium": 15, "High": 10, "Critical": 6}[priority]
        resolution_time = max(0.5, np.random.exponential(priority_base) / skill)

        # ---- Status ----------------------------------------------------
        # Tickets created closer to the dataset's end date are less
        # likely to be resolved yet (mirrors real-world pipeline state).
        days_since_creation = (end_date - ticket_date).days
        if days_since_creation < 2:
            status = np.random.choice(["Open", "In Progress"], p=[0.6, 0.4])
        elif days_since_creation < 7:
            status = np.random.choice(
                ["Open", "In Progress", "Resolved", "Closed"], p=[0.15, 0.25, 0.30, 0.30]
            )
        else:
            status = np.random.choice(
                ["Open", "In Progress", "Resolved", "Closed"], p=[0.04, 0.06, 0.30, 0.60]
            )

        # ---- Escalation --------------------------------------------
        escalation_prob = {"Low": 0.03, "Medium": 0.08, "High": 0.18, "Critical": 0.35}[priority]
        escalated = "Yes" if random.random() < escalation_prob else "No"

        # ---- Customer Satisfaction Rating (1-5) ------------------------
        # Only resolved/closed tickets realistically get a CSAT rating.
        if status in ["Resolved", "Closed"]:
            csat_base = 4.3 - (resolution_time / 40) - (0.5 if escalated == "Yes" else 0)
            csat = np.clip(np.random.normal(csat_base, 0.8), 1, 5)
            csat_rating = int(round(csat))
        else:
            csat_rating = np.nan

        records.append({
            "Ticket_ID": ticket_id,
            "Customer_ID": customer_id,
            "Ticket_Date": ticket_date.strftime("%Y-%m-%d %H:%M:%S"),
            "Issue_Category": issue_category,
            "Product_Category": product_category,
            "Priority": priority,
            "Status": status,
            "Assigned_Agent": agent,
            "Response_Time_Hours": round(response_time, 2),
            "Resolution_Time_Hours": round(resolution_time, 2) if status in ["Resolved", "Closed"] else np.nan,
            "Customer_Satisfaction_Rating": csat_rating,
            "Region": region,
            "Channel": channel,
            "Escalated": escalated,
        })

    df = pd.DataFrame(records)

    # ------------------------------------------------------------------
    # Deliberately inject realistic "dirty data" so the cleaning steps
    # in the notebook have something genuine to fix.
    # ------------------------------------------------------------------
    dirty_idx = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
    df.loc[dirty_idx, "Customer_Satisfaction_Rating"] = np.nan

    dirty_idx2 = np.random.choice(df.index, size=int(0.015 * len(df)), replace=False)
    df.loc[dirty_idx2, "Region"] = None

    # Duplicate ~1% of rows to simulate accidental double-logging
    dup_rows = df.sample(frac=0.01, random_state=SEED)
    df = pd.concat([df, dup_rows], ignore_index=True)

    # Shuffle final dataset
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = generate_dataset()
    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "customer_support_tickets.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset generated: {out_path}")
    print(f"Total records (including intentional duplicates): {len(df)}")
    print(df.head())
