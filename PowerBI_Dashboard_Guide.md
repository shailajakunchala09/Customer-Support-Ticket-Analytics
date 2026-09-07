# Power BI Dashboard — Design Guide

This guide walks through building a professional, single-page (plus drill-through)
Power BI dashboard on top of `data/customer_support_tickets_cleaned.csv`
(or the `tickets` SQL table). It's written so you can follow it step-by-step
even if you've never opened Power BI before.

---

## 1. Data Load & Modeling

1. **Get Data → Text/CSV** → select `customer_support_tickets_cleaned.csv`
   (or **Get Data → SQL Server/MySQL** if you loaded the SQL schema).
2. In **Power Query Editor**, verify/set data types:
   - `Ticket_Date` → Date/Time
   - `Resolution_Time_Hours`, `Response_Time_Hours` → Decimal Number
   - `Customer_Satisfaction_Rating` → Whole Number
   - `Priority`, `Status`, `Region`, `Channel`, `Issue_Category` → Text
3. Create a **Date table** (Modeling → New Table):
   ```
   DateTable = CALENDAR(MIN(tickets[Ticket_Date]), MAX(tickets[Ticket_Date]))
   ```
   Mark it as a Date Table, and relate it to `tickets[Ticket_Date]` (1-to-many).
4. Load the table and rename it `Tickets` in the model view.

---

## 2. DAX Measures

Create these measures in a dedicated **Measures** table for cleanliness:

```DAX
Total Tickets = COUNTROWS(Tickets)

Open Tickets = CALCULATE([Total Tickets], Tickets[Status] = "Open")

In Progress Tickets = CALCULATE([Total Tickets], Tickets[Status] = "In Progress")

Resolved Tickets = CALCULATE([Total Tickets], Tickets[Status] = "Resolved")

Closed Tickets = CALCULATE([Total Tickets], Tickets[Status] = "Closed")

Avg Resolution Time (Hrs) =
    ROUND(AVERAGE(Tickets[Resolution_Time_Hours]), 2)

Avg Response Time (Hrs) =
    ROUND(AVERAGE(Tickets[Response_Time_Hours]), 2)

Avg CSAT =
    ROUND(AVERAGE(Tickets[Customer_Satisfaction_Rating]), 2)

SLA Met Tickets =
    CALCULATE(
        [Total Tickets],
        Tickets[Resolution_Time_Hours] <= Tickets[SLA_Target_Hours]
    )

SLA Compliance % =
    DIVIDE([SLA Met Tickets], [Resolved Tickets] + [Closed Tickets], 0)

Escalated Tickets = CALCULATE([Total Tickets], Tickets[Escalated] = "Yes")

Escalation Rate % = DIVIDE([Escalated Tickets], [Total Tickets], 0)

Tickets MoM % Change =
    VAR CurrentMonth = [Total Tickets]
    VAR PrevMonth = CALCULATE([Total Tickets], DATEADD(DateTable[Date], -1, MONTH))
    RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0)
```

---

## 3. Page Layout — "Support Operations Overview"

**Top strip — KPI Cards (use Card visuals):**
`Total Tickets` | `Open Tickets` | `Closed Tickets` | `Avg Resolution Time (Hrs)` | `Avg CSAT` | `SLA Compliance %`

**Row 2 (left → right):**
- **Line Chart:** Ticket Trend by Month → X: `DateTable[Month]`, Y: `[Total Tickets]`
- **Donut Chart:** Resolution Status → `Status` legend, `[Total Tickets]` values

**Row 3:**
- **Horizontal Bar Chart:** Ticket Category Distribution → `Issue_Category` vs `[Total Tickets]`, sorted descending
- **Map / Filled Map visual:** Region-wise Analysis → `Region` on location, `[Total Tickets]` or `[Avg CSAT]` as color saturation

**Row 4:**
- **Bar Chart:** Agent Performance → `Assigned_Agent` vs `[Avg CSAT]`, secondary measure `[Avg Resolution Time (Hrs)]` on a combo chart
- **Pie Chart:** Priority Distribution → `Priority` legend, `[Total Tickets]` values
- **Gauge Visual:** SLA Compliance % (target = 90%)

**Slicers panel (left side, synced across pages):**
- `Priority` (buttons)
- `Region` (dropdown)
- `Channel` (buttons)
- `DateTable[Date]` (between slider, relative date filter)
- `Assigned_Agent` (searchable dropdown)

---

## 4. Drill-Through Page — "Agent Deep Dive"

Right-click an agent bar → **Drill through** to a page showing:
- Agent's ticket list (Table visual with conditional formatting on SLA breach)
- Agent's monthly trend line
- Agent's CSAT distribution histogram

---

## 5. Formatting & Theme

- Use a consistent corporate palette: primary `#2E86AB`, accent `#F24236`, neutral greys for backgrounds.
- Apply **View → Themes → Custom theme** with a JSON theme file for consistency across visuals.
- Add a top banner with company logo placeholder + report title + last refresh date (`"Last Refreshed: " & FORMAT(NOW(), "DD MMM YYYY")` as a text card).
- Use tooltips: enable **Report Page Tooltips** with a mini card showing ticket count + CSAT when hovering over a region/agent.

---

## 6. Interactivity Checklist

- [ ] Cross-filtering enabled between all visuals on the page
- [ ] Slicers synced across "Overview" and "Agent Deep Dive" pages (Sync Slicers pane)
- [ ] Bookmarks for two views: "Executive Summary" (KPI cards + trend only) and "Detailed Ops View" (all visuals)
- [ ] Mobile layout configured (Power BI Mobile Layout view) for the KPI cards

---

## 7. Publishing

1. File → Publish → Publish to Power BI service.
2. Set up a **Scheduled Refresh** (daily) if connected to a live SQL source.
3. Export a PDF/PNG snapshot of the final dashboard into `screenshots/dashboard_overview.png` for the README.

> **Note:** Since this repository is designed to run without a Power BI license
> for reviewers, the `.pbix` file (if you build one) should be added to the
> `dashboard/` folder, and a static screenshot exported to `screenshots/`
> so the dashboard is visible directly from GitHub's README preview.
