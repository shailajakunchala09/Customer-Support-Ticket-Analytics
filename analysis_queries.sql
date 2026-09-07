/* ============================================================================
   Customer Support Ticket Analysis - SQL Analysis Scripts
   ----------------------------------------------------------------------------
   Target: The 'tickets' table created via schema.sql, loaded from
   data/customer_support_tickets_cleaned.csv

   Compatible with MySQL / PostgreSQL / SQL Server (minor syntax notes added
   where dialects differ, e.g. date-truncation functions).
   ============================================================================ */


-- ----------------------------------------------------------------------------
-- 1. TOP ISSUE CATEGORIES BY TICKET VOLUME
-- ----------------------------------------------------------------------------
SELECT
    issue_category,
    COUNT(*)                                    AS total_tickets,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM tickets
GROUP BY issue_category
ORDER BY total_tickets DESC;


-- ----------------------------------------------------------------------------
-- 2. AVERAGE RESOLUTION TIME (OVERALL, AND BY PRIORITY)
-- ----------------------------------------------------------------------------
-- Overall average resolution time
SELECT ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time_hours
FROM tickets
WHERE resolution_time_hours IS NOT NULL;

-- Average resolution time by priority level
SELECT
    priority,
    ROUND(AVG(resolution_time_hours), 2)   AS avg_resolution_time_hours,
    ROUND(MIN(resolution_time_hours), 2)   AS min_resolution_time_hours,
    ROUND(MAX(resolution_time_hours), 2)   AS max_resolution_time_hours,
    COUNT(*)                               AS resolved_ticket_count
FROM tickets
WHERE resolution_time_hours IS NOT NULL
GROUP BY priority
ORDER BY avg_resolution_time_hours DESC;


-- ----------------------------------------------------------------------------
-- 3. OPEN vs CLOSED (FULL STATUS BREAKDOWN)
-- ----------------------------------------------------------------------------
SELECT
    status,
    COUNT(*)                                            AS ticket_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)  AS pct_of_total
FROM tickets
GROUP BY status
ORDER BY ticket_count DESC;


-- ----------------------------------------------------------------------------
-- 4. AGENT PERFORMANCE SCORECARD
-- ----------------------------------------------------------------------------
SELECT
    assigned_agent,
    COUNT(*)                                                     AS tickets_handled,
    ROUND(AVG(resolution_time_hours), 2)                         AS avg_resolution_time_hours,
    ROUND(AVG(customer_satisfaction_rating), 2)                  AS avg_csat,
    ROUND(100.0 * SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS escalation_rate_pct
FROM tickets
GROUP BY assigned_agent
ORDER BY avg_csat DESC, avg_resolution_time_hours ASC;


-- ----------------------------------------------------------------------------
-- 5. MONTHLY TICKET TRENDS
-- ----------------------------------------------------------------------------
-- MySQL / PostgreSQL syntax using DATE_FORMAT / TO_CHAR respectively.
-- MySQL version:
SELECT
    DATE_FORMAT(ticket_date, '%Y-%m')  AS ticket_month,
    COUNT(*)                           AS total_tickets
FROM tickets
GROUP BY DATE_FORMAT(ticket_date, '%Y-%m')
ORDER BY ticket_month;

-- PostgreSQL equivalent:
-- SELECT TO_CHAR(ticket_date, 'YYYY-MM') AS ticket_month, COUNT(*) AS total_tickets
-- FROM tickets
-- GROUP BY TO_CHAR(ticket_date, 'YYYY-MM')
-- ORDER BY ticket_month;


-- ----------------------------------------------------------------------------
-- 6. CUSTOMER SATISFACTION BY REGION
-- ----------------------------------------------------------------------------
SELECT
    region,
    ROUND(AVG(customer_satisfaction_rating), 2)  AS avg_csat,
    COUNT(*)                                     AS ticket_count
FROM tickets
WHERE customer_satisfaction_rating IS NOT NULL
GROUP BY region
ORDER BY avg_csat DESC;


-- ----------------------------------------------------------------------------
-- 7. ESCALATED TICKETS ANALYSIS
-- ----------------------------------------------------------------------------
-- Escalation rate by priority
SELECT
    priority,
    COUNT(*)                                                                  AS total_tickets,
    SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END)                        AS escalated_tickets,
    ROUND(100.0 * SUM(CASE WHEN escalated = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS escalation_rate_pct
FROM tickets
GROUP BY priority
ORDER BY escalation_rate_pct DESC;

-- Escalated tickets by issue category
SELECT
    issue_category,
    COUNT(*) AS escalated_ticket_count
FROM tickets
WHERE escalated = 'Yes'
GROUP BY issue_category
ORDER BY escalated_ticket_count DESC;


-- ----------------------------------------------------------------------------
-- 8. HIGH-PRIORITY UNRESOLVED TICKETS (OPERATIONAL BOTTLENECK VIEW)
-- ----------------------------------------------------------------------------
SELECT
    ticket_id,
    customer_id,
    priority,
    status,
    assigned_agent,
    ticket_date,
    region,
    channel
FROM tickets
WHERE priority IN ('High', 'Critical')
  AND status NOT IN ('Resolved', 'Closed')
ORDER BY
    CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 END,
    ticket_date ASC;


-- ----------------------------------------------------------------------------
-- BONUS 9. SLA COMPLIANCE RATE (Overall & by Priority)
-- ----------------------------------------------------------------------------
-- Assumes a sla_target_hours column exists (see schema.sql) or is computed
-- inline via a CASE expression as shown below.
SELECT
    priority,
    COUNT(*)                                                                          AS resolved_tickets,
    SUM(CASE
            WHEN resolution_time_hours <= CASE priority
                    WHEN 'Critical' THEN 6
                    WHEN 'High'     THEN 12
                    WHEN 'Medium'   THEN 24
                    WHEN 'Low'      THEN 48
                 END
            THEN 1 ELSE 0
        END)                                                                          AS sla_met_count,
    ROUND(100.0 * SUM(CASE
            WHEN resolution_time_hours <= CASE priority
                    WHEN 'Critical' THEN 6
                    WHEN 'High'     THEN 12
                    WHEN 'Medium'   THEN 24
                    WHEN 'Low'      THEN 48
                 END
            THEN 1 ELSE 0
        END) / COUNT(*), 2)                                                           AS sla_compliance_pct
FROM tickets
WHERE resolution_time_hours IS NOT NULL
GROUP BY priority
ORDER BY sla_compliance_pct ASC;


-- ----------------------------------------------------------------------------
-- BONUS 10. CHANNEL-WISE PERFORMANCE
-- ----------------------------------------------------------------------------
SELECT
    channel,
    COUNT(*)                                       AS total_tickets,
    ROUND(AVG(response_time_hours), 2)             AS avg_response_time_hours,
    ROUND(AVG(resolution_time_hours), 2)           AS avg_resolution_time_hours,
    ROUND(AVG(customer_satisfaction_rating), 2)    AS avg_csat
FROM tickets
GROUP BY channel
ORDER BY total_tickets DESC;


-- ----------------------------------------------------------------------------
-- BONUS 11. TOP 5 CUSTOMERS BY TICKET VOLUME (identifying at-risk / high-touch accounts)
-- ----------------------------------------------------------------------------
SELECT
    customer_id,
    COUNT(*) AS ticket_count,
    ROUND(AVG(customer_satisfaction_rating), 2) AS avg_csat
FROM tickets
GROUP BY customer_id
ORDER BY ticket_count DESC
LIMIT 5;


-- ----------------------------------------------------------------------------
-- BONUS 12. WEEKDAY DEMAND PATTERN (staffing/scheduling insight)
-- ----------------------------------------------------------------------------
-- MySQL: DAYNAME(); PostgreSQL: TO_CHAR(ticket_date, 'Day')
SELECT
    DAYNAME(ticket_date) AS weekday,
    COUNT(*)             AS ticket_count
FROM tickets
GROUP BY DAYNAME(ticket_date)
ORDER BY ticket_count DESC;
