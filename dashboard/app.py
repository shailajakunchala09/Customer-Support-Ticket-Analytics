import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Support Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM DARK THEME COLORS
# ============================================================

BG = "#080B0F"
SIDEBAR_BG = "#0C1117"

CARD_BG = "#111820"
CARD_BG_2 = "#151D26"

BORDER = "#26313D"

TEXT_PRIMARY = "#F5F7FA"
TEXT_SECONDARY = "#B4BEC9"
TEXT_MUTED = "#7E8A97"

ACCENT = "#4DA3FF"
ACCENT_LIGHT = "#7DBBFF"

SUCCESS = "#35D07F"
WARNING = "#FFB84D"
DANGER = "#FF5C6C"
PURPLE = "#8B6CFF"
CYAN = "#36D1DC"

PLOT_BG = "#111820"
GRID = "#26313D"


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    f"""
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {{
        background: {BG};
        color: {TEXT_PRIMARY};
    }}

    [data-testid="stAppViewContainer"] {{
        background: {BG};
    }}

    [data-testid="stHeader"] {{
        background: {BG};
    }}

    [data-testid="stToolbar"] {{
        background: transparent;
    }}

    .main {{
        background: {BG};
    }}

    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {{
        background: {SIDEBAR_BG};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT_PRIMARY};
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {TEXT_PRIMARY} !important;
    }}

    [data-testid="stSidebar"] label {{
        color: {TEXT_SECONDARY} !important;
        font-weight: 600;
    }}

    /* ========================================================
       HEADINGS
       ======================================================== */

    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_PRIMARY} !important;
    }}

    p {{
        color: {TEXT_SECONDARY};
    }}

    /* ========================================================
       HERO SECTION
       ======================================================== */

    .hero {{
        background:
            radial-gradient(
                circle at top right,
                rgba(77,163,255,0.13),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #111922 0%,
                #0B1016 55%,
                #101721 100%
            );

        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 34px 38px;
        margin-bottom: 24px;

        box-shadow:
            0 15px 45px rgba(0,0,0,0.35);
    }}

    .hero-badge {{
        display: inline-block;
        background: rgba(77,163,255,0.10);
        border: 1px solid rgba(77,163,255,0.30);
        color: {ACCENT_LIGHT};
        padding: 6px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.7px;
        margin-bottom: 14px;
    }}

    .hero-title {{
        color: {TEXT_PRIMARY};
        font-size: 40px;
        font-weight: 850;
        letter-spacing: -1.2px;
        line-height: 1.15;
        margin: 0;
    }}

    .hero-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 16px;
        margin-top: 11px;
        line-height: 1.6;
        max-width: 900px;
    }}

    .hero-status {{
        margin-top: 18px;
        color: {SUCCESS};
        font-size: 13px;
        font-weight: 700;
    }}

    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {{
        background:
            linear-gradient(
                145deg,
                {CARD_BG_2},
                {CARD_BG}
            );

        border: 1px solid {BORDER};
        border-radius: 17px;
        padding: 21px 22px;
        min-height: 132px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.22);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(77,163,255,0.65);
        box-shadow:
            0 12px 32px rgba(0,0,0,0.35);
    }}

    .kpi-icon {{
        font-size: 20px;
        margin-bottom: 7px;
    }}

    .kpi-label {{
        color: {TEXT_MUTED};
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}

    .kpi-value {{
        color: {TEXT_PRIMARY};
        font-size: 30px;
        font-weight: 850;
        line-height: 1.15;
        margin-top: 6px;
    }}

    .kpi-caption {{
        color: {TEXT_SECONDARY};
        font-size: 11px;
        margin-top: 7px;
    }}

    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {{
        color: {TEXT_PRIMARY};
        font-size: 22px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }}

    .section-subtitle {{
        color: {TEXT_MUTED};
        font-size: 13px;
        margin-bottom: 15px;
    }}

    /* ========================================================
       FILTER CARD
       ======================================================== */

    .filter-header {{
        color: {TEXT_PRIMARY};
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 5px;
    }}

    .filter-description {{
        color: {TEXT_MUTED};
        font-size: 12px;
        margin-bottom: 15px;
    }}

    /* ========================================================
       STREAMLIT SELECTBOX
       ======================================================== */

    [data-baseweb="select"] > div {{
        background: {CARD_BG} !important;
        border-color: {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
    }}

    [data-baseweb="select"] span {{
        color: {TEXT_PRIMARY} !important;
    }}

    [data-baseweb="popover"] {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
    }}

    /* ========================================================
       INPUTS
       ======================================================== */

    input {{
        background: {CARD_BG} !important;
        color: {TEXT_PRIMARY} !important;
        border-color: {BORDER} !important;
    }}

    /* ========================================================
       DATE INPUT
       ======================================================== */

    [data-testid="stDateInput"] input {{
        color: {TEXT_PRIMARY} !important;
        background: {CARD_BG} !important;
    }}

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {{
        width: 100%;
        background: {CARD_BG};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 10px;
        font-weight: 700;
        min-height: 42px;
    }}

    .stButton > button:hover {{
        border-color: {ACCENT};
        color: {ACCENT_LIGHT};
        background: #17212C;
    }}

    /* ========================================================
       DOWNLOAD BUTTON
       ======================================================== */

    .stDownloadButton > button {{
        background: {ACCENT};
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-weight: 750;
        min-height: 42px;
    }}

    .stDownloadButton > button:hover {{
        background: {ACCENT_LIGHT};
        color: #071019;
    }}

    /* ========================================================
       METRIC / ALERT TEXT
       ======================================================== */

    [data-testid="stMetricValue"] {{
        color: {TEXT_PRIMARY} !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {TEXT_SECONDARY} !important;
    }}

    /* ========================================================
       DATAFRAME
       ======================================================== */

    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 13px;
        overflow: hidden;
    }}

    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}

    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {{
        border-color: {BORDER};
    }}

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {{
        border-top: 1px solid {BORDER};
        margin-top: 35px;
        padding: 24px 0 8px 0;
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 12px;
    }}

    .footer strong {{
        color: {TEXT_SECONDARY};
    }}

    </style>
    """
)


# ============================================================
# DATA LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "customer_support_tickets_cleaned.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Convert date
    df["Ticket_Date"] = pd.to_datetime(
        df["Ticket_Date"],
        errors="coerce"
    )

    # Numeric columns
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

    return df


try:
    df = load_data()
except Exception as e:
    st.error("Unable to load the customer support dataset.")
    st.code(str(e))
    st.stop()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def boolean_series(series):
    """
    Converts common True/False and Yes/No values
    into a boolean Series.
    """
    if series.dtype == bool:
        return series

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "y"])
    )


def chart_layout(fig, height=380):
    """
    Applies consistent premium dark styling to Plotly charts.
    """

    fig.update_layout(
        template="plotly_dark",
        height=height,

        paper_bgcolor=BG,
        plot_bgcolor=PLOT_BG,

        font=dict(
            color=TEXT_PRIMARY,
            family="Arial, sans-serif"
        ),

        title_font=dict(
            color=TEXT_PRIMARY,
            size=17
        ),

        margin=dict(
            l=25,
            r=25,
            t=60,
            b=25
        ),

        hoverlabel=dict(
            bgcolor="#1B2530",
            bordercolor=BORDER,
            font=dict(
                color=TEXT_PRIMARY
            )
        ),

        legend=dict(
            font=dict(
                color=TEXT_SECONDARY
            )
        )
    )

    fig.update_xaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        color=TEXT_SECONDARY
    )

    fig.update_yaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        color=TEXT_SECONDARY
    )

    return fig


def section_header(title, subtitle=None):
    if subtitle:
        st.html(
            f"""
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
            """
        )
    else:
        st.html(
            f"""
            <div class="section-title">{title}</div>
            """
        )


# ============================================================
# PREPARE DATA
# ============================================================

df["Is_Resolved_Bool"] = boolean_series(
    df["Is_Resolved"]
)

df["SLA_Met_Bool"] = boolean_series(
    df["SLA_Met"]
)

df["Escalated_Bool"] = boolean_series(
    df["Escalated"]
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div style="
            font-size:25px;
            font-weight:850;
            color:#F5F7FA;
            margin-bottom:4px;
        ">
            📊 Analytics
        </div>

        <div style="
            color:#7E8A97;
            font-size:12px;
            margin-bottom:20px;
        ">
            Customer Support Intelligence
        </div>
        """
    )

    st.markdown("---")

    st.html(
        """
        <div class="filter-header">
            🔎 Dashboard Filters
        </div>

        <div class="filter-description">
            Refine the analytics using the filters below.
        </div>
        """
    )

    # Priority
    priority_options = ["All"] + sorted(
        df["Priority"].dropna().unique().tolist()
    )

    selected_priority = st.selectbox(
        "Priority",
        priority_options
    )

    # Status
    status_options = ["All"] + sorted(
        df["Status"].dropna().unique().tolist()
    )

    selected_status = st.selectbox(
        "Status",
        status_options
    )

    # Issue Category
    issue_options = ["All"] + sorted(
        df["Issue_Category"].dropna().unique().tolist()
    )

    selected_issue = st.selectbox(
        "Issue Category",
        issue_options
    )

    # Region
    region_options = ["All"] + sorted(
        df["Region"].dropna().unique().tolist()
    )

    selected_region = st.selectbox(
        "Region",
        region_options
    )

    # Channel
    channel_options = ["All"] + sorted(
        df["Channel"].dropna().unique().tolist()
    )

    selected_channel = st.selectbox(
        "Support Channel",
        channel_options
    )

    # Date range
    min_date = df["Ticket_Date"].min().date()
    max_date = df["Ticket_Date"].max().date()

    selected_dates = st.date_input(
        "Ticket Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("")

    if st.button("↻ Reset Filters"):

        st.rerun()

    st.markdown("---")

    st.html(
        f"""
        <div style="
            background:{CARD_BG};
            border:1px solid {BORDER};
            border-radius:12px;
            padding:14px;
        ">

            <div style="
                color:{TEXT_MUTED};
                font-size:11px;
                text-transform:uppercase;
                letter-spacing:0.7px;
                font-weight:700;
            ">
                Dataset
            </div>

            <div style="
                color:{TEXT_PRIMARY};
                font-size:18px;
                font-weight:800;
                margin-top:5px;
            ">
                {len(df):,} Tickets
            </div>

            <div style="
                color:{TEXT_MUTED};
                font-size:11px;
                margin-top:4px;
            ">
                Customer Support Dataset
            </div>

        </div>
        """
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_priority != "All":
    filtered_df = filtered_df[
        filtered_df["Priority"] == selected_priority
    ]


if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["Status"] == selected_status
    ]


if selected_issue != "All":
    filtered_df = filtered_df[
        filtered_df["Issue_Category"] == selected_issue
    ]


if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if selected_channel != "All":
    filtered_df = filtered_df[
        filtered_df["Channel"] == selected_channel
    ]


if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])

    end_date = (
        pd.Timestamp(selected_dates[1])
        + pd.Timedelta(days=1)
    )

    filtered_df = filtered_df[
        (filtered_df["Ticket_Date"] >= start_date)
        &
        (filtered_df["Ticket_Date"] < end_date)
    ]


# ============================================================
# HERO HEADER
# ============================================================

resolved_count = int(
    filtered_df["Is_Resolved_Bool"].sum()
)

total_count = len(filtered_df)

resolution_rate = (
    resolved_count / total_count * 100
    if total_count > 0
    else 0
)

st.html(
    f"""
    <div class="hero">

        <div class="hero-badge">
            CUSTOMER SUPPORT INTELLIGENCE
        </div>

        <div class="hero-title">
            Customer Support Analytics
        </div>

        <div class="hero-subtitle">
            A professional analytics dashboard for monitoring
            ticket volume, customer satisfaction, resolution
            efficiency, SLA compliance, escalation patterns,
            and agent performance.
        </div>

        <div class="hero-status">
            ● Live dashboard &nbsp; | &nbsp;
            {total_count:,} filtered tickets &nbsp; | &nbsp;
            {resolution_rate:.1f}% resolution rate
        </div>

    </div>
    """
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_tickets = len(filtered_df)

resolved_tickets = int(
    filtered_df["Is_Resolved_Bool"].sum()
)

resolution_rate = (
    resolved_tickets / total_tickets * 100
    if total_tickets > 0
    else 0
)

avg_resolution = (
    filtered_df["Resolution_Time_Hours"].mean()
    if total_tickets > 0
    else 0
)

avg_response = (
    filtered_df["Response_Time_Hours"].mean()
    if total_tickets > 0
    else 0
)

avg_csat = (
    filtered_df["Customer_Satisfaction_Rating"].mean()
    if total_tickets > 0
    else 0
)

sla_rate = (
    filtered_df["SLA_Met_Bool"].mean() * 100
    if total_tickets > 0
    else 0
)

escalated_count = int(
    filtered_df["Escalated_Bool"].sum()
)

escalation_rate = (
    escalated_count / total_tickets * 100
    if total_tickets > 0
    else 0
)


# ============================================================
# KPI SECTION
# ============================================================

section_header(
    "Performance Overview",
    "Key customer support performance indicators"
)


kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🎫</div>

            <div class="kpi-label">
                Total Tickets
            </div>

            <div class="kpi-value">
                {total_tickets:,}
            </div>

            <div class="kpi-caption">
                Filtered support requests
            </div>

        </div>
        """
    )


with kpi2:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">✅</div>

            <div class="kpi-label">
                Resolved Tickets
            </div>

            <div class="kpi-value">
                {resolved_tickets:,}
            </div>

            <div class="kpi-caption">
                Successfully resolved
            </div>

        </div>
        """
    )


with kpi3:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">📈</div>

            <div class="kpi-label">
                Resolution Rate
            </div>

            <div class="kpi-value">
                {resolution_rate:.1f}%
            </div>

            <div class="kpi-caption">
                Overall resolution efficiency
            </div>

        </div>
        """
    )


kpi4, kpi5, kpi6 = st.columns(3)

with kpi4:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">⏱️</div>

            <div class="kpi-label">
                Avg Resolution
            </div>

            <div class="kpi-value">
                {avg_resolution:.1f}h
            </div>

            <div class="kpi-caption">
                Average resolution time
            </div>

        </div>
        """
    )


with kpi5:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">⭐</div>

            <div class="kpi-label">
                Avg CSAT
            </div>

            <div class="kpi-value">
                {avg_csat:.2f}/5
            </div>

            <div class="kpi-caption">
                Customer satisfaction
            </div>

        </div>
        """
    )


with kpi6:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🎯</div>

            <div class="kpi-label">
                SLA Compliance
            </div>

            <div class="kpi-value">
                {sla_rate:.1f}%
            </div>

            <div class="kpi-caption">
                Tickets meeting SLA
            </div>

        </div>
        """
    )


# ============================================================
# MONTHLY TICKET TREND
# ============================================================

section_header(
    "Ticket Volume Trend",
    "Monthly customer support demand over time"
)


if not filtered_df.empty:

    monthly = (
        filtered_df
        .groupby("Ticket_Month")
        .size()
        .reset_index(name="Tickets")
    )

    monthly = monthly.sort_values("Ticket_Month")

    fig_monthly = px.area(
        monthly,
        x="Ticket_Month",
        y="Tickets",
        markers=True
    )

    fig_monthly.update_traces(
        line=dict(
            color=ACCENT,
            width=3
        ),
        marker=dict(
            size=7,
            color=ACCENT
        ),
        fillcolor="rgba(77,163,255,0.15)"
    )

    fig_monthly.update_layout(
        title="Monthly Ticket Volume",
        xaxis_title="Month",
        yaxis_title="Number of Tickets"
    )

    fig_monthly = chart_layout(
        fig_monthly,
        410
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

else:
    st.info("No data available for the selected filters.")


# ============================================================
# STATUS + ISSUE CATEGORY
# ============================================================

section_header(
    "Support Operations",
    "Ticket status and issue category distribution"
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# STATUS DONUT
# ------------------------------------------------------------

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
        hole=0.60
    )

    fig_status.update_traces(
        textposition="outside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color=BG,
                width=3
            )
        )
    )

    fig_status.update_layout(
        title="Ticket Status",
        showlegend=True
    )

    fig_status = chart_layout(
        fig_status,
        390
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# ------------------------------------------------------------
# ISSUE CATEGORY
# ------------------------------------------------------------

with col2:

    issue_data = (
        filtered_df["Issue_Category"]
        .value_counts()
        .reset_index()
    )

    issue_data.columns = [
        "Issue_Category",
        "Tickets"
    ]

    issue_data = issue_data.sort_values(
        "Tickets",
        ascending=True
    )

    fig_issue = px.bar(
        issue_data,
        x="Tickets",
        y="Issue_Category",
        orientation="h"
    )

    fig_issue.update_traces(
        marker_color=ACCENT,
        marker_line_width=0
    )

    fig_issue.update_layout(
        title="Issue Category Distribution",
        xaxis_title="Tickets",
        yaxis_title=""
    )

    fig_issue = chart_layout(
        fig_issue,
        390
    )

    st.plotly_chart(
        fig_issue,
        use_container_width=True
    )


# ============================================================
# PRIORITY + CHANNEL
# ============================================================

section_header(
    "Ticket Composition",
    "Priority levels and support channels"
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# PRIORITY
# ------------------------------------------------------------

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
        y="Tickets"
    )

    fig_priority.update_traces(
        marker_color=PURPLE
    )

    fig_priority.update_layout(
        title="Priority Distribution",
        xaxis_title="Priority",
        yaxis_title="Tickets"
    )

    fig_priority = chart_layout(
        fig_priority,
        370
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True
    )


# ------------------------------------------------------------
# CHANNEL
# ------------------------------------------------------------

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
        y="Tickets"
    )

    fig_channel.update_traces(
        marker_color=CYAN
    )

    fig_channel.update_layout(
        title="Support Channel Distribution",
        xaxis_title="Channel",
        yaxis_title="Tickets"
    )

    fig_channel = chart_layout(
        fig_channel,
        370
    )

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )


# ============================================================
# REGIONAL SUPPORT VOLUME
# ============================================================

section_header(
    "Regional Analysis",
    "Customer support demand across regions"
)


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
    text="Tickets"
)

fig_region.update_traces(
    marker_color=ACCENT,
    textposition="outside"
)

fig_region.update_layout(
    title="Regional Support Volume",
    xaxis_title="Region",
    yaxis_title="Tickets"
)

fig_region = chart_layout(
    fig_region,
    390
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# ============================================================
# CUSTOMER SATISFACTION
# ============================================================

section_header(
    "Customer Satisfaction",
    "Distribution of customer satisfaction ratings"
)


csat_data = (
    filtered_df["Customer_Satisfaction_Rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

csat_data.columns = [
    "Rating",
    "Tickets"
]

csat_data["Rating"] = csat_data["Rating"].astype(str)


fig_csat = px.bar(
    csat_data,
    x="Rating",
    y="Tickets",
    text="Tickets"
)

fig_csat.update_traces(
    marker_color=SUCCESS,
    textposition="outside"
)

fig_csat.update_layout(
    title="Customer Satisfaction Rating Distribution",
    xaxis_title="Rating",
    yaxis_title="Tickets"
)

fig_csat = chart_layout(
    fig_csat,
    380
)

st.plotly_chart(
    fig_csat,
    use_container_width=True
)


# ============================================================
# RESOLUTION TIME BY PRIORITY
# ============================================================

section_header(
    "Resolution Efficiency",
    "Resolution-time variation across ticket priorities"
)


fig_resolution = px.box(
    filtered_df,
    x="Priority",
    y="Resolution_Time_Hours",
    points="outliers"
)

fig_resolution.update_traces(
    marker_color=ACCENT_LIGHT,
    line_color=ACCENT
)

fig_resolution.update_layout(
    title="Resolution Time by Priority",
    xaxis_title="Priority",
    yaxis_title="Resolution Time (Hours)"
)

fig_resolution = chart_layout(
    fig_resolution,
    420
)

st.plotly_chart(
    fig_resolution,
    use_container_width=True
)


# ============================================================
# SLA + ESCALATION
# ============================================================

section_header(
    "SLA & Escalation",
    "Operational compliance and escalation monitoring"
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# SLA
# ------------------------------------------------------------

with col1:

    sla_data = pd.DataFrame(
        {
            "SLA Status": [
                "Met",
                "Missed"
            ],
            "Tickets": [
                int(filtered_df["SLA_Met_Bool"].sum()),
                int(
                    (~filtered_df["SLA_Met_Bool"])
                    .sum()
                )
            ]
        }
    )

    fig_sla = px.pie(
        sla_data,
        names="SLA Status",
        values="Tickets",
        hole=0.60
    )

    fig_sla.update_traces(
        textposition="outside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color=BG,
                width=3
            )
        )
    )

    fig_sla.update_layout(
        title="SLA Compliance"
    )

    fig_sla = chart_layout(
        fig_sla,
        390
    )

    st.plotly_chart(
        fig_sla,
        use_container_width=True
    )


# ------------------------------------------------------------
# ESCALATION
# ------------------------------------------------------------

with col2:

    escalation_data = pd.DataFrame(
        {
            "Escalation Status": [
                "Escalated",
                "Not Escalated"
            ],
            "Tickets": [
                int(filtered_df["Escalated_Bool"].sum()),
                int(
                    (~filtered_df["Escalated_Bool"])
                    .sum()
                )
            ]
        }
    )

    fig_escalation = px.pie(
        escalation_data,
        names="Escalation Status",
        values="Tickets",
        hole=0.60
    )

    fig_escalation.update_traces(
        textposition="outside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color=BG,
                width=3
            )
        )
    )

    fig_escalation.update_layout(
        title="Escalation Analysis"
    )

    fig_escalation = chart_layout(
        fig_escalation,
        390
    )

    st.plotly_chart(
        fig_escalation,
        use_container_width=True
    )


# ============================================================
# RESPONSE VS RESOLUTION
# ============================================================

section_header(
    "Response & Resolution Relationship",
    "Understanding how response time relates to total resolution time"
)


scatter_df = filtered_df[
    [
        "Response_Time_Hours",
        "Resolution_Time_Hours",
        "Priority",
        "Customer_Satisfaction_Rating"
    ]
].dropna()


if not scatter_df.empty:

    fig_scatter = px.scatter(
        scatter_df,
        x="Response_Time_Hours",
        y="Resolution_Time_Hours",
        color="Priority",
        size="Customer_Satisfaction_Rating",
        hover_data=[
            "Customer_Satisfaction_Rating"
        ],
        opacity=0.70
    )

    fig_scatter.update_layout(
        title="Response Time vs Resolution Time",
        xaxis_title="Response Time (Hours)",
        yaxis_title="Resolution Time (Hours)"
    )

    fig_scatter = chart_layout(
        fig_scatter,
        430
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# ============================================================
# AGENT PERFORMANCE
# ============================================================

section_header(
    "Agent Performance",
    "Support agent workload, satisfaction and resolution performance"
)


if not filtered_df.empty:

    agent_data = (
        filtered_df
        .groupby("Assigned_Agent")
        .agg(
            Tickets=("Ticket_ID", "count"),
            Avg_CSAT=(
                "Customer_Satisfaction_Rating",
                "mean"
            ),
            Avg_Response_Hours=(
                "Response_Time_Hours",
                "mean"
            ),
            Avg_Resolution_Hours=(
                "Resolution_Time_Hours",
                "mean"
            ),
            SLA_Compliance=(
                "SLA_Met_Bool",
                "mean"
            )
        )
        .reset_index()
    )

    agent_data["SLA_Compliance"] = (
        agent_data["SLA_Compliance"] * 100
    )

    agent_data = agent_data.sort_values(
        "Tickets",
        ascending=False
    )

    display_agents = agent_data.copy()

    display_agents["Avg_CSAT"] = (
        display_agents["Avg_CSAT"]
        .round(2)
    )

    display_agents["Avg_Response_Hours"] = (
        display_agents["Avg_Response_Hours"]
        .round(2)
    )

    display_agents["Avg_Resolution_Hours"] = (
        display_agents["Avg_Resolution_Hours"]
        .round(2)
    )

    display_agents["SLA_Compliance"] = (
        display_agents["SLA_Compliance"]
        .round(1)
    )

    display_agents = display_agents.rename(
        columns={
            "Assigned_Agent": "Agent",
            "Tickets": "Tickets",
            "Avg_CSAT": "Avg CSAT",
            "Avg_Response_Hours": "Avg Response (h)",
            "Avg_Resolution_Hours": "Avg Resolution (h)",
            "SLA_Compliance": "SLA Compliance (%)"
        }
    )

    st.dataframe(
        display_agents,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TOP PERFORMING AGENTS
# ============================================================

section_header(
    "Top Performing Agents",
    "Agents ranked by customer satisfaction"
)


if not filtered_df.empty:

    top_agents = (
        agent_data
        .sort_values(
            "Avg_CSAT",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Avg_CSAT",
            ascending=True
        )
    )

    fig_agents = px.bar(
        top_agents,
        x="Avg_CSAT",
        y="Assigned_Agent",
        orientation="h",
        text="Avg_CSAT"
    )

    fig_agents.update_traces(
        marker_color=SUCCESS,
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_agents.update_layout(
        title="Top 10 Agents by Average CSAT",
        xaxis_title="Average CSAT",
        yaxis_title=""
    )

    fig_agents = chart_layout(
        fig_agents,
        430
    )

    st.plotly_chart(
        fig_agents,
        use_container_width=True
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

section_header(
    "Key Business Insights",
    "Automatically generated observations from the filtered dataset"
)


# Most common issue
if not filtered_df.empty:

    most_common_issue = (
        filtered_df["Issue_Category"]
        .value_counts()
        .idxmax()
    )

    issue_count = (
        filtered_df["Issue_Category"]
        .value_counts()
        .max()
    )

    # Most common channel
    most_common_channel = (
        filtered_df["Channel"]
        .value_counts()
        .idxmax()
    )

    # Highest ticket priority
    priority_counts = (
        filtered_df["Priority"]
        .value_counts()
    )

    highest_priority = (
        priority_counts.idxmax()
        if not priority_counts.empty
        else "N/A"
    )

    # Best region by CSAT
    regional_csat = (
        filtered_df
        .groupby("Region")[
            "Customer_Satisfaction_Rating"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    best_region = (
        regional_csat.index[0]
        if not regional_csat.empty
        else "N/A"
    )

    best_region_csat = (
        regional_csat.iloc[0]
        if not regional_csat.empty
        else 0
    )

    insight1, insight2 = st.columns(2)

    with insight1:

        st.html(
            f"""
            <div style="
                background:{CARD_BG};
                border:1px solid {BORDER};
                border-radius:15px;
                padding:20px;
                min-height:145px;
            ">

                <div style="
                    color:{ACCENT};
                    font-size:13px;
                    font-weight:800;
                    text-transform:uppercase;
                    letter-spacing:0.7px;
                ">
                    🔎 Most Common Issue
                </div>

                <div style="
                    color:{TEXT_PRIMARY};
                    font-size:21px;
                    font-weight:800;
                    margin-top:9px;
                ">
                    {most_common_issue}
                </div>

                <div style="
                    color:{TEXT_SECONDARY};
                    font-size:13px;
                    margin-top:7px;
                ">
                    {issue_count:,} tickets are associated
                    with this issue category.
                </div>

            </div>
            """
        )

    with insight2:

        st.html(
            f"""
            <div style="
                background:{CARD_BG};
                border:1px solid {BORDER};
                border-radius:15px;
                padding:20px;
                min-height:145px;
            ">

                <div style="
                    color:{CYAN};
                    font-size:13px;
                    font-weight:800;
                    text-transform:uppercase;
                    letter-spacing:0.7px;
                ">
                    📞 Leading Channel
                </div>

                <div style="
                    color:{TEXT_PRIMARY};
                    font-size:21px;
                    font-weight:800;
                    margin-top:9px;
                ">
                    {most_common_channel}
                </div>

                <div style="
                    color:{TEXT_SECONDARY};
                    font-size:13px;
                    margin-top:7px;
                ">
                    This is the most frequently used
                    customer support channel.
                </div>

            </div>
            """
        )


    insight3, insight4 = st.columns(2)

    with insight3:

        st.html(
            f"""
            <div style="
                background:{CARD_BG};
                border:1px solid {BORDER};
                border-radius:15px;
                padding:20px;
                margin-top:14px;
                min-height:145px;
            ">

                <div style="
                    color:{WARNING};
                    font-size:13px;
                    font-weight:800;
                    text-transform:uppercase;
                    letter-spacing:0.7px;
                ">
                    ⚡ Dominant Priority
                </div>

                <div style="
                    color:{TEXT_PRIMARY};
                    font-size:21px;
                    font-weight:800;
                    margin-top:9px;
                ">
                    {highest_priority}
                </div>

                <div style="
                    color:{TEXT_SECONDARY};
                    font-size:13px;
                    margin-top:7px;
                ">
                    This priority represents the largest
                    share of filtered tickets.
                </div>

            </div>
            """
        )

    with insight4:

        st.html(
            f"""
            <div style="
                background:{CARD_BG};
                border:1px solid {BORDER};
                border-radius:15px;
                padding:20px;
                margin-top:14px;
                min-height:145px;
            ">

                <div style="
                    color:{SUCCESS};
                    font-size:13px;
                    font-weight:800;
                    text-transform:uppercase;
                    letter-spacing:0.7px;
                ">
                    🏆 Best Region by CSAT
                </div>

                <div style="
                    color:{TEXT_PRIMARY};
                    font-size:21px;
                    font-weight:800;
                    margin-top:9px;
                ">
                    {best_region}
                </div>

                <div style="
                    color:{TEXT_SECONDARY};
                    font-size:13px;
                    margin-top:7px;
                ">
                    Average customer satisfaction:
                    {best_region_csat:.2f}/5
                </div>

            </div>
            """
        )


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

section_header(
    "Dashboard Summary",
    "Overall operational snapshot"
)


summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(
        "Average Response Time",
        f"{avg_response:.2f} hrs"
    )


with summary_col2:

    st.metric(
        "Escalation Rate",
        f"{escalation_rate:.1f}%"
    )


with summary_col3:

    st.metric(
        "Filtered Records",
        f"{total_tickets:,}"
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div class="footer">

        <strong>
            Customer Support Analytics Dashboard
        </strong>

        <br>

        Built with Streamlit • Pandas • Plotly

        <br>

        <span>
            Interactive analytics for customer support
            operations and business decision-making.
        </span>

    </div>
    """
)