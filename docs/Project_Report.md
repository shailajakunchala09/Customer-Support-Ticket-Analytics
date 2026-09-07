# Project Report: Customer Support Ticket Analysis

## 1. Executive Summary

This report documents an end-to-end analysis of 12,000 customer support
tickets generated over a 12-month period. The objective was to evaluate
support operations performance, identify bottlenecks, and provide the
business with concrete, prioritized recommendations to improve customer
satisfaction and operational efficiency. The analysis covered data cleaning,
exploratory data analysis, KPI computation, SQL-based reporting, and Power BI
dashboard design.

## 2. Business Context

Support organizations are judged on three things: **speed** (how quickly
tickets are acknowledged and resolved), **quality** (whether the resolution
satisfies the customer), and **efficiency** (how well resources — agents,
channels, budget — are being used). This project models a mid-size company's
support function, handling tickets across 12 issue categories, 8 product
lines, 5 regions, 4 channels, and a 15-person agent team.

## 3. Data Overview

- **Source:** Synthetically generated (`src/generate_dataset.py`) to mirror a
  real ticketing system export, including realistic "dirty data" (duplicates,
  missing values) so the cleaning process reflects genuine data engineering work.
- **Volume:** 12,120 raw rows → 12,000 after deduplication.
- **Time span:** January 2024 – December 2024.
- **Grain:** One row per support ticket.

## 4. Methodology

### 4.1 Data Cleaning
- Removed 120 duplicate ticket rows (`Ticket_ID`-based).
- Standardized data types (dates, numerics, categoricals).
- Filled missing `Region` values with "Unknown" rather than dropping rows,
  preserving ticket volume for trend analysis.
- Imputed missing CSAT ratings for resolved/closed tickets using the median
  rating for that issue category, avoiding bias from simply dropping rows.
- Left `Resolution_Time_Hours` and CSAT as null for tickets that are
  genuinely still open — this is structurally correct, not "missing data."

### 4.2 Feature Engineering
- `Ticket_Month`, `Ticket_Weekday` for trend/seasonality analysis.
- `SLA_Target_Hours` mapped by priority (Critical: 6h, High: 12h, Medium: 24h, Low: 48h).
- `SLA_Met` flag comparing actual resolution time against the target.

### 4.3 Analysis Performed
- KPI computation (volume, resolution/response time, CSAT, SLA compliance, escalation rate)
- Monthly trend analysis
- Issue-category and product-category breakdowns
- Agent performance scorecarding
- Resolution-time distribution by priority
- Regional CSAT comparison
- Escalation-rate analysis by priority
- SQL-based reporting layer mirroring the Python analysis for a data-warehouse context

## 5. Key Findings

| # | Finding |
|---|---|
| 1 | Feature Requests, Refund Requests, and Account Access are the top 3 issue categories (~26% of volume combined) |
| 2 | Overall SLA compliance is ~80%; Critical-priority tickets are the highest-risk segment |
| 3 | Escalation rate rises sharply with priority — Critical tickets escalate far more than Low priority |
| 4 | Phone and Chat channels resolve faster on average than Email and Web |
| 5 | Agent performance (CSAT, resolution time, SLA compliance) varies meaningfully across the 15-agent team |
| 6 | Regional CSAT is relatively even (3.81–3.84 out of 5), indicating consistent customer experience delivery |

## 6. Business Recommendations

1. Deploy self-service resources (FAQ/chatbot) for the top 3 issue categories to reduce ticket inflow.
2. Introduce a fast-lane triage process for Critical/High priority tickets to protect SLA compliance.
3. Launch structured coaching for lower-performing agents using top performers' patterns as a benchmark.
4. Encourage customers with urgent issues toward Phone/Chat channels.
5. Automate CSAT-at-close prompts to reduce missing-rating data quality issues.
6. Establish a monthly SLA and escalation-rate review cadence by priority tier.

## 7. Limitations

- The dataset is synthetically generated; while distributions and correlations
  were designed to mirror real support operations, real production data may
  reveal additional patterns (e.g. product-specific seasonality, agent
  tenure effects) not modeled here.
- CSAT is only available for resolved/closed tickets, consistent with how
  most real systems collect it — but this means the "true" satisfaction of
  customers with still-open tickets is unknown at analysis time.

## 8. Conclusion

The support operation analyzed here handles a high ticket volume with
generally consistent regional customer experience, but has clear improvement
opportunities in SLA compliance for urgent tickets and in leveling up
lower-performing agents. Implementing the recommendations above — self-service
deflection, priority-based triage, and targeted coaching — should measurably
improve both CSAT and operational efficiency within 1–2 quarters.

---
*Prepared as part of the Customer Support Ticket Analysis portfolio project. See the accompanying Jupyter notebook (`notebooks/Customer_Support_Ticket_Analysis.ipynb`) for the full analysis code and charts.*
