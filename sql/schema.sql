/* ============================================================================
   Customer Support Ticket Analysis - Database Schema
   ----------------------------------------------------------------------------
   Creates the `tickets` table used by analysis_queries.sql.
   Written in ANSI-compatible SQL (tested against MySQL 8 / PostgreSQL 14).
   ============================================================================ */

DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    ticket_id                      VARCHAR(20)     PRIMARY KEY,
    customer_id                    VARCHAR(20)     NOT NULL,
    ticket_date                    DATETIME        NOT NULL,
    issue_category                 VARCHAR(50)     NOT NULL,
    product_category                VARCHAR(50)     NOT NULL,
    priority                        VARCHAR(10)     NOT NULL,   -- Low, Medium, High, Critical
    status                          VARCHAR(15)     NOT NULL,   -- Open, In Progress, Resolved, Closed
    assigned_agent                  VARCHAR(50)     NOT NULL,
    response_time_hours            DECIMAL(6,2),
    resolution_time_hours          DECIMAL(6,2),
    customer_satisfaction_rating   TINYINT,                     -- 1-5, NULL for unresolved tickets
    region                          VARCHAR(20),
    channel                         VARCHAR(10),                 -- Email, Chat, Phone, Web
    escalated                       VARCHAR(3)      NOT NULL,    -- Yes / No
    sla_target_hours               DECIMAL(5,2)
);

-- Helpful indexes for the query patterns used in analysis_queries.sql
CREATE INDEX idx_tickets_status ON tickets (status);
CREATE INDEX idx_tickets_priority ON tickets (priority);
CREATE INDEX idx_tickets_agent ON tickets (assigned_agent);
CREATE INDEX idx_tickets_region ON tickets (region);
CREATE INDEX idx_tickets_date ON tickets (ticket_date);

/* ----------------------------------------------------------------------------
   Loading the cleaned CSV (MySQL example -- adjust path & permissions):

   LOAD DATA LOCAL INFILE 'data/customer_support_tickets_cleaned.csv'
   INTO TABLE tickets
   FIELDS TERMINATED BY ','
   OPTIONALLY ENCLOSED BY '"'
   LINES TERMINATED BY '\n'
   IGNORE 1 ROWS
   (ticket_id, customer_id, ticket_date, issue_category, product_category,
    priority, status, assigned_agent, response_time_hours, resolution_time_hours,
    customer_satisfaction_rating, region, channel, escalated, @ticket_month,
    @ticket_weekday, @is_resolved, sla_target_hours, @sla_met);

   PostgreSQL example:

   COPY tickets(ticket_id, customer_id, ticket_date, issue_category, product_category,
                priority, status, assigned_agent, response_time_hours, resolution_time_hours,
                customer_satisfaction_rating, region, channel, escalated, sla_target_hours)
   FROM 'data/customer_support_tickets_cleaned.csv'
   DELIMITER ','
   CSV HEADER;
---------------------------------------------------------------------------- */
