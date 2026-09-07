# Interview Questions & Answers — Customer Support Ticket Analysis

Use these to prepare for interview walkthroughs of this project. Answers are
written to be spoken naturally — adapt the specifics (numbers, tools) to your
actual results if you regenerate the dataset.

---

### 1. Walk me through this project end-to-end.

I analyzed a synthetic dataset of 12,000 customer support tickets modeled on
a real support operation — tickets across 12 categories, 5 regions, 4
channels, and 15 agents over a full year. I built a Python cleaning
pipeline to handle duplicates and missing values, then did EDA and KPI
analysis to measure resolution time, SLA compliance, CSAT, and escalation
rate. I mirrored the same analysis in SQL for a data-warehouse context, and
designed a Power BI dashboard for executive reporting. I finished with a
written report translating the findings into business recommendations.

### 2. Why did you choose this business problem?

Customer support is a function every company has, and it produces rich,
measurable operational data — perfect for demonstrating the full analytics
lifecycle: cleaning, EDA, KPI reporting, SQL, and dashboarding, all tied back
to a business outcome (customer satisfaction and efficiency) that's easy for
any interviewer to relate to.

### 3. How did you handle missing data, and why that approach?

I used different strategies depending on *why* the data was missing. Missing
`Region` values were filled with "Unknown" rather than dropped, since
dropping would have lost real ticket volume. Missing CSAT for resolved
tickets was imputed with the median rating for that issue category — a more
representative fill than the overall mean. But for `Resolution_Time_Hours`
on tickets that are still open, I left it as null intentionally, because
that's not missing data — it structurally doesn't exist yet.

### 4. How did you detect and handle duplicates?

I deduplicated on `Ticket_ID`, keeping the first occurrence, since a
duplicate ticket ID represents the same support event being logged twice —
not two separate legitimate tickets.

### 5. What KPIs did you calculate, and why those specifically?

Total tickets, open/closed breakdown, average resolution and response time,
average CSAT, SLA compliance rate, and escalation rate. These map directly
to the three things support leadership cares about: volume/capacity, speed,
and quality — plus SLA compliance and escalation rate as leading indicators
of operational risk.

### 6. What is SLA compliance, and how did you calculate it?

SLA (Service Level Agreement) compliance measures what percentage of
resolved tickets were resolved within their target time window. I set
priority-based targets (Critical: 6 hrs, High: 12 hrs, Medium: 24 hrs, Low:
48 hrs) and calculated a boolean `SLA_Met` flag per ticket, then averaged
it — both overall and broken down by agent, priority, and category.

### 7. What was the most interesting insight you found?

Escalation rate rose sharply with priority — Critical-priority tickets
escalated far more often than Low-priority ones. Combined with SLA data
showing Critical tickets also had the tightest compliance margins, that
pointed to a clear operational bottleneck: the team's biggest risk area is
handling urgent tickets fast enough, not overall volume.

### 8. How did you measure agent performance, and how would you use it responsibly?

I built a scorecard per agent: tickets handled, average resolution time,
average CSAT, SLA compliance %, and escalation rate. I'd use this for
coaching and identifying best practices from top performers — not for
punitive action alone, since ticket difficulty/category mix can differ
between agents and should be accounted for before drawing conclusions.

### 9. Why use both Python and SQL in the same project?

They serve different purposes. Python/Pandas is great for iterative,
exploratory analysis, visualization, and feature engineering. SQL is how
this kind of data usually lives in production — in a warehouse — so I wrote
equivalent queries to show I can extract the same insights directly from a
database, which is closer to how a working data analyst would actually
interact with this data day-to-day.

### 10. Explain one of your SQL queries in detail.

The SLA compliance query groups tickets by priority, then for each priority
tier, compares `resolution_time_hours` against a CASE expression that maps
priority to its SLA target hours, counting how many tickets met that target.
Dividing that count by the resolved-ticket count per priority gives the
compliance percentage — the same logic as the Python `SLA_Met` flag, just
expressed declaratively in SQL.

### 11. How would you design this differently if the data were real and continuously growing?

I'd move from a static CSV to a proper pipeline — ingesting tickets on a
schedule (e.g. via Airflow), loading into a warehouse table with the schema
I already defined, and connecting Power BI with a scheduled refresh instead
of a manual CSV import. I'd also add data-quality checks (e.g. Great
Expectations) to catch schema drift or unexpected nulls automatically.

### 12. What would you add if you had more time?

A machine learning model to predict at ticket-creation time whether it's
likely to escalate or breach SLA, so it can be proactively prioritized. I'd
also add NLP sentiment analysis on ticket text if free-text descriptions
were available, and a lightweight Streamlit app as an alternative to Power BI
for teams without a BI license.

### 13. Why did you pick a synthetic dataset instead of a public one?

I wanted full control over the data's structure and realism — including
deliberately injecting duplicates and missing values so the cleaning steps
in the project are genuine, not just for show. I also built in realistic
correlations (e.g. priority affecting resolution time, channel affecting
response time, agent skill variance) so the analysis has real patterns to
uncover rather than pure noise.

### 14. How did you validate that your synthetic data is "realistic"?

I anchored the generation logic in domain knowledge about how support
operations actually behave: higher-severity tickets get worked faster in
relative terms but are often harder so still take longer overall; phone/chat
respond faster than email; tickets closer to the reporting cutoff are less
likely to be resolved yet. These aren't arbitrary — they mirror patterns
you'd expect to see (and can verify) in a real support dataset.

### 15. What's the difference between resolution time and response time in your analysis?

Response time is how long it took an agent to first acknowledge/respond to
a ticket. Resolution time is how long until the ticket was fully resolved.
They measure different things — response time reflects triage speed,
resolution time reflects total effort/complexity — so I analyzed them
separately rather than combining them into one metric.

### 16. How would you present these findings to a non-technical stakeholder?

I'd lead with the Power BI dashboard and 3-4 headline numbers (total
tickets, SLA compliance, CSAT, escalation rate), then walk through 2-3
concrete recommendations tied to the data — e.g. "SLA compliance drops to
X% for Critical tickets; a dedicated triage lane for these could close
most of that gap." I'd avoid leading with methodology unless asked.

### 17. What assumptions did you make in this analysis, and where might they break down?

I assumed SLA targets are uniform by priority level company-wide, which may
not hold if different product lines have different contractual SLAs. I also
assumed missing region values could be reasonably grouped as "Unknown"
rather than geo-inferred from other fields — in a real dataset, I'd check if
there's a more reliable way to backfill that (e.g. from customer account data).

### 18. How did you ensure your code is production-quality, not just notebook code?

I separated reusable logic into modules (`data_cleaning.py`, `kpi_analysis.py`,
`visualization.py`) with docstrings, type-annotated function signatures,
logging instead of print statements, and explicit exception handling for
file I/O. The notebook then imports and calls these modules rather than
duplicating logic inline, so the same code could be reused in a script or
pipeline.

### 19. What was the hardest part of this project?

Getting the missing-value strategy right for CSAT — deciding it should
differ by whether a ticket was actually resolved, and if resolved, imputing
per issue-category rather than a single global fill. It's a small design
decision, but it's the kind of judgment call that matters in real analytics
work and is easy to get lazily wrong.

### 20. Why should a company care about the metrics you calculated?

Because they connect directly to retention and cost. SLA breaches and low
CSAT drive churn and increase support cost through repeat contacts and
escalations. Measuring these consistently — and tying them to specific,
fixable causes like priority-tier triage or agent coaching gaps — is what
turns a support team from a cost center into a lever for customer
retention.

---

## STAR-Based Explanation (for behavioral-style interview rounds)

**Situation:** A (simulated) company was receiving thousands of customer
support tickets monthly with no structured way to measure performance,
identify bottlenecks, or report to leadership.

**Task:** I set out to build a complete analytics solution — from raw,
messy ticket data to a leadership-ready dashboard and a set of concrete
business recommendations — that could plausibly be handed to a real support
operations team.

**Action:** I generated a realistic 12,000-record dataset with intentional
data-quality issues, built a modular Python cleaning pipeline with proper
logging and exception handling, performed EDA and KPI analysis (SLA
compliance, CSAT, escalation rate, agent performance), replicated the core
analysis in SQL for a data-warehouse context, and designed a Power BI
dashboard with DAX measures and interactive filters. I documented everything
in a project report.

**Result:** The finished analysis surfaced a clear, actionable pattern —
SLA compliance and escalation risk both concentrate heavily in Critical
priority tickets — and I translated that into a specific recommendation
(a fast-lane triage process) that a real support team could implement
directly. The project also gave me hands-on practice with the full
analytics stack a data analyst role actually uses day-to-day: Python, SQL,
and BI tooling together, not in isolation.
