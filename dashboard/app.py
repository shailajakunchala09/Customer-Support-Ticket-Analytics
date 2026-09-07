import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Support Ticket Analytics",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL DASHBOARD STYLING
# =========================================================

st.markdown("""
<style>

    /* Main application */
    .stApp {
        background-color: #f5f7fb;
    }

    .main {
        padding-top: 1rem;
    }

    /* Main title */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 750 !important;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-weight: 650 !important;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e4e7ec;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
        min-height: 120px;
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 750;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e4e7ec;
    }

    section[data-testid="stSidebar"] h2 {
        font-weight: 700 !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #667085;
        font-size: 0.9rem;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "customer_support_tickets_cleaned.csv"


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "❌ Dataset not found.\n\n"
        f"Expected location:\n{DATA_PATH}"
    )
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

# Convert numeric columns safely
numeric_columns = [
    "Response_Time_Hours",
    "Resolution_Time_Hours",
    "Customer_Satisfaction_Rating",
    "SLA_Target_Hours",
    "SLA_Met"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# Convert resolution/responses to numeric
df["Resolution_Time_Hours"] = pd.to_numeric(
    df["Resolution_Time_Hours"],
    errors="coerce"
)

df["Customer_Satisfaction_Rating"] = pd.to_numeric(
    df["Customer_Satisfaction_Rating"],
    errors="coerce"
)


# =========================================================
# HEADER
# =========================================================

st.title("🎫 Customer Support Ticket Analytics")

st.markdown(
    "### Interactive Support Operations & Customer Experience Dashboard"
)

st.caption(
    "Analyze ticket volume, resolution performance, SLA compliance, "
    "customer satisfaction and agent performance."
)

st.success(
    f"✅ Dataset loaded successfully — {len(df):,} customer support tickets"
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.caption(
    "Use the filters below to explore the support data."
)


# Priority
priority_options = sorted(
    df["Priority"].dropna().unique()
)

priority_filter = st.sidebar.multiselect(
    "Priority",
    options=priority_options,
    default=priority_options
)


# Status
status_options = sorted(
    df["Status"].dropna().unique()
)

status_filter = st.sidebar.multiselect(
    "Status",
    options=status_options,
    default=status_options
)


# Issue Category
category_options = sorted(
    df["Issue_Category"].dropna().unique()
)

category_filter = st.sidebar.multiselect(
    "Issue Category",
    options=category_options,
    default=category_options
)


# Region
region_options = sorted(
    df["Region"].dropna().unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options
)


# Channel
channel_options = sorted(
    df["Channel"].dropna().unique()
)

channel_filter = st.sidebar.multiselect(
    "Channel",
    options=channel_options,
    default=channel_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Priority"].isin(priority_filter))
    & (df["Status"].isin(status_filter))
    & (df["Issue_Category"].isin(category_filter))
    & (df["Region"].isin(region_filter))
    & (df["Channel"].isin(channel_filter))
].copy()


# =========================================================
# NO DATA MESSAGE
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No tickets match the selected filters. "
        "Please change the filters in the sidebar."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_tickets = len(filtered_df)


resolved_tickets = int(
    filtered_df["Is_Resolved"].sum()
)


resolution_rate = (
    resolved_tickets / total_tickets * 100
)


avg_resolution = (
    filtered_df["Resolution_Time_Hours"].mean()
)


avg_csat = (
    filtered_df["Customer_Satisfaction_Rating"].mean()
)


sla_compliance = (
    filtered_df["SLA_Met"].mean() * 100
)


# =========================================================
# KPI SECTION
# =========================================================

st.divider()

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.metric(
        "🎫 Total Tickets",
        f"{total_tickets:,}"
    )


with col2:

    st.metric(
        "✅ Resolved",
        f"{resolved_tickets:,}"
    )


with col3:

    st.metric(
        "📈 Resolution Rate",
        f"{resolution_rate:.1f}%"
    )


with col4:

    st.metric(
        "⏱️ Avg Resolution",
        f"{avg_resolution:.1f} hrs"
    )


with col5:

    st.metric(
        "⭐ Avg CSAT",
        f"{avg_csat:.2f}/5"
    )


with col6:

    st.metric(
        "🎯 SLA Compliance",
        f"{sla_compliance:.1f}%"
    )


# =========================================================
# TICKET ANALYTICS
# =========================================================

st.divider()

st.subheader("📈 Ticket Analytics")


# ---------------------------------------------------------
# MONTHLY TICKET VOLUME
# ---------------------------------------------------------

monthly = (
    filtered_df
    .groupby("Ticket_Month")
    .size()
    .reset_index(name="Tickets")
)

monthly = monthly.sort_values("Ticket_Month")


fig_monthly = px.line(
    monthly,
    x="Ticket_Month",
    y="Tickets",
    markers=True,
    title="Monthly Ticket Volume"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Tickets",
    hovermode="x unified"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# =========================================================
# STATUS + CATEGORY
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# STATUS DISTRIBUTION
# ---------------------------------------------------------

with col1:

    status_data = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Tickets"
    ]

    fig_status = px.pie(
        status_data,
        names="Status",
        values="Tickets",
        title="Ticket Status Distribution",
        hole=0.45
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# ---------------------------------------------------------
# ISSUE CATEGORY
# ---------------------------------------------------------

with col2:

    category_data = (
        filtered_df["Issue_Category"]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Issue Category",
        "Tickets"
    ]

    fig_category = px.bar(
        category_data,
        x="Tickets",
        y="Issue Category",
        orientation="h",
        title="Tickets by Issue Category",
        text="Tickets"
    )

    fig_category.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# =========================================================
# PRIORITY + CHANNEL
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# PRIORITY
# ---------------------------------------------------------

with col1:

    priority_data = (
        filtered_df["Priority"]
        .value_counts()
        .reset_index()
    )

    priority_data.columns = [
        "Priority",
        "Tickets"
    ]

    fig_priority = px.bar(
        priority_data,
        x="Priority",
        y="Tickets",
        title="Tickets by Priority",
        text="Tickets"
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True
    )


# ---------------------------------------------------------
# CHANNEL
# ---------------------------------------------------------

with col2:

    channel_data = (
        filtered_df["Channel"]
        .value_counts()
        .reset_index()
    )

    channel_data.columns = [
        "Channel",
        "Tickets"
    ]

    fig_channel = px.bar(
        channel_data,
        x="Channel",
        y="Tickets",
        title="Tickets by Support Channel",
        text="Tickets"
    )

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )


# =========================================================
# REGION
# =========================================================

st.subheader("🌍 Regional Ticket Analysis")


region_data = (
    filtered_df["Region"]
    .value_counts()
    .reset_index()
)

region_data.columns = [
    "Region",
    "Tickets"
]


fig_region = px.bar(
    region_data,
    x="Region",
    y="Tickets",
    title="Tickets by Region",
    text="Tickets"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# =========================================================
# RESOLUTION & SLA PERFORMANCE
# =========================================================

st.divider()

st.subheader("⏱️ Resolution & SLA Performance")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# RESOLUTION TIME DISTRIBUTION
# ---------------------------------------------------------

with col1:

    fig_resolution = px.histogram(
        filtered_df,
        x="Resolution_Time_Hours",
        nbins=30,
        title="Resolution Time Distribution",
        labels={
            "Resolution_Time_Hours":
            "Resolution Time (Hours)"
        }
    )

    st.plotly_chart(
        fig_resolution,
        use_container_width=True
    )


# ---------------------------------------------------------
# SLA COMPLIANCE
# ---------------------------------------------------------

with col2:

    sla_data = (
        filtered_df["SLA_Met"]
        .map({
            1.0: "SLA Met",
            0.0: "SLA Missed"
        })
        .value_counts()
        .reset_index()
    )

    sla_data.columns = [
        "SLA Status",
        "Tickets"
    ]

    fig_sla = px.pie(
        sla_data,
        names="SLA Status",
        values="Tickets",
        title="SLA Compliance",
        hole=0.45
    )

    st.plotly_chart(
        fig_sla,
        use_container_width=True
    )


# =========================================================
# ESCALATION ANALYSIS
# =========================================================

st.subheader("🚨 Escalation Analysis")


escalation_data = (
    filtered_df["Escalated"]
    .value_counts()
    .reset_index()
)

escalation_data.columns = [
    "Escalated",
    "Tickets"
]


fig_escalation = px.bar(
    escalation_data,
    x="Escalated",
    y="Tickets",
    title="Escalated vs Non-Escalated Tickets",
    text="Tickets"
)

st.plotly_chart(
    fig_escalation,
    use_container_width=True
)


# =========================================================
# AGENT PERFORMANCE
# =========================================================

st.divider()

st.subheader("👨‍💼 Agent Performance")


agent_performance = (
    filtered_df
    .groupby("Assigned_Agent")
    .agg(
        Tickets=("Ticket_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        Avg_CSAT=(
            "Customer_Satisfaction_Rating",
            "mean"
        ),

        SLA_Compliance=(
            "SLA_Met",
            "mean"
        ),

        Escalated_Tickets=(
            "Escalated",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)


agent_performance["SLA_Compliance"] = (
    agent_performance["SLA_Compliance"] * 100
)


agent_performance = (
    agent_performance
    .sort_values(
        "Tickets",
        ascending=False
    )
)


st.dataframe(
    agent_performance.style.format({
        "Avg_Resolution_Hours": "{:.2f}",
        "Avg_CSAT": "{:.2f}",
        "SLA_Compliance": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TOP PERFORMING AGENTS
# =========================================================

st.subheader("🏆 Top Performing Agents")


top_agents = (
    agent_performance
    .sort_values(
        ["Avg_CSAT", "SLA_Compliance"],
        ascending=False
    )
    .head(5)
)


st.dataframe(
    top_agents.style.format({
        "Avg_Resolution_Hours": "{:.2f}",
        "Avg_CSAT": "{:.2f}",
        "SLA_Compliance": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DATASET SUMMARY
# =========================================================

st.divider()

st.subheader("📋 Dataset Summary")


summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.info(
        f"**Filtered Tickets**\n\n"
        f"{len(filtered_df):,}"
    )


with summary_col2:

    st.info(
        f"**Support Agents**\n\n"
        f"{filtered_df['Assigned_Agent'].nunique():,}"
    )


with summary_col3:

    st.info(
        f"**Issue Categories**\n\n"
        f"{filtered_df['Issue_Category'].nunique():,}"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="dashboard-footer">
        <b>Customer Support Ticket Analytics</b><br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)