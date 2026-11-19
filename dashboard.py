import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
 
# Load environment variables
load_dotenv()
 
# --- Connect to Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
 
# --- Page Config ---
st.set_page_config(
    page_title="AI Resume Parsing Analytics Dashboard",
    layout="wide",
    page_icon=" "
)
 
# --- Custom CSS for better styling ---
st.markdown("""
<style>

/* ============================= */
/* MAIN APP BACKGROUND */
/* ============================= */

.stApp {
    background-color: #0E1117 !important;
}

.main {
    background-color: #0E1117 !important;
}

.block-container {
    background-color: #0E1117 !important;
}
/* ============================= */
/* STREAMLIT TOP HEADER / DEPLOY BAR */
/* ============================= */

[data-testid="stHeader"] {
    background-color: #0E1117 !important;
}

[data-testid="stToolbar"] {
    background-color: #0E1117 !important;
}

[data-testid="stHeader"] button {
    color: #FFFFFF !important;
}

[data-testid="stHeader"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}
            

/* ============================= */
/* SIDEBAR */
/* ============================= */

[data-testid="stSidebar"] {
    background-color: #161B22 !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}


/* ============================= */
/* HEADINGS */
/* ============================= */

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
}


/* ============================= */
/* NORMAL TEXT */
/* ============================= */

p {
    color: #E5E7EB !important;
}


/* ============================= */
/* KPI METRIC CARDS */
/* ============================= */

[data-testid="stMetric"] {
    background-color: #1F2937 !important;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #374151;
}

/* KPI Label */
[data-testid="stMetricLabel"] {
    color: #D1D5DB !important;
}

/* KPI Value */
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* KPI Delta */
[data-testid="stMetricDelta"] {
    color: #FFFFFF !important;
}


/* ============================= */
/* DARK DROPDOWN SELECT BOXES */
/* ============================= */

/* Main dropdown box */
[data-baseweb="select"] {
    background-color: #1F2937 !important;
    border-radius: 6px !important;
}

/* Dropdown inner container */
[data-baseweb="select"] > div {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
    border-color: #374151 !important;
}

/* Selected value text */
[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

/* Input text */
[data-baseweb="select"] input {
    color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
}

/* Dropdown arrow */
[data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}


/* ============================= */
/* DROPDOWN MENU */
/* ============================= */

[data-baseweb="popover"] {
    background-color: #161B22 !important;
}

[data-baseweb="menu"] {
    background-color: #161B22 !important;
}

/* Dropdown options */
[data-baseweb="menu"] li {
    background-color: #161B22 !important;
    color: #FFFFFF !important;
}

/* Dropdown option text */
[data-baseweb="menu"] li span {
    color: #FFFFFF !important;
}

/* Hover option */
[data-baseweb="menu"] li:hover {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}

/* Selected option */
[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #374151 !important;
    color: #FFFFFF !important;
}


/* ============================= */
/* USAGE LOG NUMBER DROPDOWN */
/* ============================= */

div[data-baseweb="select"] {
    background-color: #1F2937 !important;
}

div[data-baseweb="select"] > div {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

/* ============================= */
/* DATE INPUT */
/* ============================= */

[data-testid="stDateInput"] input {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}


/* ============================= */
/* DOWNLOAD BUTTON */
/* ============================= */

.stDownloadButton button {
    background-color: #059669 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}


/* ============================= */
/* INFO BOX */
/* ============================= */

[data-testid="stAlert"] {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}

[data-testid="stAlert"] p {
    color: #FFFFFF !important;
}


/* ============================= */
/* DARK HTML TABLES */
/* ============================= */

.dark-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #161B22 !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
}

/* Table Header */
.dark-table thead th {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    border-bottom: 1px solid #374151;
}

/* Table Body */
.dark-table tbody td {
    background-color: #161B22 !important;
    color: #E5E7EB !important;
    padding: 10px 15px;
    border-bottom: 1px solid #30363D;
}

/* Hover Effect */
.dark-table tbody tr:hover td {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}


/* ============================= */
/* REMOVE WHITE TABLE BACKGROUND */
/* ============================= */

.dark-table tr,
.dark-table td {
    background-color: #161B22 !important;
}

.dark-table th {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
}


/* ============================= */
/* PLOTLY CHART BACKGROUND */
/* ============================= */

.js-plotly-plot {
    background-color: #0E1117 !important;
}

</style>
""", unsafe_allow_html=True)
 
# --- Title ---
st.title("AI Resume Parsing Analytics Dashboard")
st.info("AI-powered recruitment dashboard for monitoring resume screening activity, candidate processing and system performance.")
st.markdown("---")
 
# --- Fetch Data from Supabase ---
@st.cache_data(ttl=60)
def fetch_llm_usage():
    response = supabase.table("llm_usage").select("*").execute()
    return pd.DataFrame(response.data)
 
@st.cache_data(ttl=60)
def fetch_resumes():
    response = supabase.table("resumes").select("id, username, created_at").execute()
    return pd.DataFrame(response.data)

@st.cache_data(ttl=60)
def fetch_user_details():
    response = supabase.table("user_details").select("id").execute()
    return pd.DataFrame(response.data)
 
# Load data
df = fetch_llm_usage()
resumes_df = fetch_resumes()
user_details_df = fetch_user_details()
 
# --- Data Validation ---
if df.empty:
    st.warning("No data found in llm_usage table. Please add some data first.")
    st.stop()
 
# Convert created_at to datetime
df['created_at'] = pd.to_datetime(df['created_at'])
 
# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
 
# --- Time Period Filter ---
st.sidebar.subheader("📅 Time Period")

time_period = st.sidebar.selectbox(
    "Select Period",
    [
        "All Time",
        "Today",
        "Last 7 Days",
        "Last 30 Days",
        "Last 90 Days",
        "This Month",
        "Previous Month",
        "This Year"
    ]
)
 
# Usage type filter
usage_types = ["All"] + sorted(df['usage_type'].dropna().unique().tolist())
selected_usage_type = st.sidebar.selectbox("Usage Type", usage_types)
 
# Status filter
statuses = ["All"] + sorted(df['status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Status", statuses)
 
# Username filter
usernames = ["All"] + sorted(df['username'].dropna().unique().tolist())
selected_username = st.sidebar.selectbox("Username", usernames)
 
# Apply filters
filtered_df = df.copy()

# --- Apply Time Period Filter ---

today = pd.Timestamp.now().normalize()

if time_period == "Today":

    filtered_df = filtered_df[
        filtered_df['created_at'] >= today
    ]

elif time_period == "Last 7 Days":

    start_date = today - pd.Timedelta(days=7)

    filtered_df = filtered_df[
        filtered_df['created_at'] >= start_date
    ]

elif time_period == "Last 30 Days":

    start_date = today - pd.Timedelta(days=30)

    filtered_df = filtered_df[
        filtered_df['created_at'] >= start_date
    ]

elif time_period == "Last 90 Days":

    start_date = today - pd.Timedelta(days=90)

    filtered_df = filtered_df[
        filtered_df['created_at'] >= start_date
    ]

elif time_period == "This Month":

    start_date = today.replace(day=1)

    filtered_df = filtered_df[
        filtered_df['created_at'] >= start_date
    ]

elif time_period == "Previous Month":

    first_day_current_month = today.replace(day=1)

    last_day_previous_month = (
        first_day_current_month - pd.Timedelta(days=1)
    )

    first_day_previous_month = (
        last_day_previous_month.replace(day=1)
    )

    filtered_df = filtered_df[
        (filtered_df['created_at'] >= first_day_previous_month) &
        (filtered_df['created_at'] < first_day_current_month)
    ]

elif time_period == "This Year":

    start_date = today.replace(
        month=1,
        day=1
    )

    filtered_df = filtered_df[
        filtered_df['created_at'] >= start_date
    ]
if selected_usage_type != "All":
    filtered_df = filtered_df[filtered_df['usage_type'] == selected_usage_type]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df['status'] == selected_status]
if selected_username != "All":
    filtered_df = filtered_df[filtered_df['username'] == selected_username]
if filtered_df.empty:
    st.warning(
        "⚠️ No data available for the selected filters. "
        "Please select a different time period or filter."
    )
    st.stop()
 
# --- KPI Cards ---
st.subheader("📊 Key Metrics")
 
col1, col2, col3, col4, col5 = st.columns(5)
 
with col1:
    st.metric("Total API Calls", len(filtered_df))
 
with col2:
    success_rate = (filtered_df['status'] == 'success').mean() * 100
    st.metric("Success Rate", f"{success_rate:.1f}%")
 
with col3:
    total_cost = filtered_df['total_cost'].sum()
    st.metric("Total Cost", f"${total_cost:.4f}")
 
with col4:
    total_users = len(user_details_df)
    st.metric("Total Users", total_users)
 
with col5:
    active_users = filtered_df['username'].nunique()
    st.metric("Active Users", active_users)
 
st.markdown("---")
 
# --- Row 1: Charts ---
col1, col2 = st.columns(2)
 
with col1:
    st.subheader("📈 Token Usage Trend")
    daily_tokens = filtered_df.groupby(filtered_df['created_at'].dt.date)['total_tokens'].sum()
    fig1 = px.area(
        x=daily_tokens.index,
        y=daily_tokens.values,
        title="Daily Token Consumption",
        labels={'x': 'Date', 'y': 'Tokens'}
    )
    fig1.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))
    
    st.plotly_chart(fig1, use_container_width=True)
 
with col2:
    st.subheader("🔥 Usage Activity Heatmap")
    filtered_df['day'] = filtered_df['created_at'].dt.day_name()
    filtered_df['hour'] = filtered_df['created_at'].dt.hour

    heatmap = filtered_df.groupby(
        ['day', 'hour']
    ).size().reset_index(name='count')
    fig2 = px.density_heatmap(
        heatmap,
        x='hour',
        y='day',
        z='count',
        title='Usage Activity by Hour and Day'
    )
    fig2.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))

    st.plotly_chart(fig2, use_container_width=True)


# --- Row 2: Usage Type Distribution ---
col1, col2 = st.columns(2)
 
with col1:
    st.subheader("📋 Usage Type Distribution")
    usage_counts = filtered_df['usage_type'].value_counts()
    fig3 = px.pie(
        values=usage_counts.values,
        names=usage_counts.index,
        title="API Calls by Usage Type",
        hole=0.3
    )
    fig3.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))

    st.plotly_chart(fig3, use_container_width=True)
 
with col2:
    st.subheader("📅 Monthly Usage Trend")

    monthly = filtered_df.groupby(
    filtered_df['created_at'].dt.to_period("M")
    ).size()

    fig4 = px.line(
        x=monthly.index.astype(str),
        y=monthly.values,
        markers=True,
        title="Monthly API Usage"
    )
    fig4.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))

    st.plotly_chart(fig4, use_container_width=True)
 
# --- Row 3: Token Usage Analysis ---
st.subheader("🪙 Token Usage Analysis")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_input_tokens = filtered_df['input_tokens'].mean()
    st.metric("Avg Input Tokens", f"{avg_input_tokens:.0f}")
 
with col2:
    avg_output_tokens = filtered_df['output_tokens'].mean()
    st.metric("Avg Output Tokens", f"{avg_output_tokens:.0f}")
 
with col3:
    avg_total_tokens = filtered_df['total_tokens'].mean()
    st.metric("Avg Total Tokens", f"{avg_total_tokens:.0f}")
 
# Token ratio
filtered_df['output_input_ratio'] = filtered_df['output_tokens'] / filtered_df['input_tokens'].replace(0, 1)
fig5 = px.box(
    filtered_df,
    x='usage_type',
    y='output_input_ratio',
    title='Output/Input Token Ratio by Usage Type',
    labels={'usage_type': 'Usage Type', 'output_input_ratio': 'Output/Input Ratio'}
)
fig5.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))

st.plotly_chart(fig5, use_container_width=True)

 
# --- Row 4: Cost Trend Over Time ---
st.subheader("Cost Trend Over")
daily_cost = (
    filtered_df.groupby(filtered_df["created_at"].dt.date)["total_cost"]
    .sum()
)

fig6= px.line(
    x=daily_cost.index,
    y=daily_cost.values,
    markers=True,
    title="Daily AI Cost"
)
fig6.update_layout(template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"))

st.plotly_chart(fig6,use_container_width=True)
 
# --- Row 5: Top Users ---
st.subheader("🏆 Top Users by Token Usage")

top_users = filtered_df.groupby('username').agg({
    'total_tokens': 'sum',
    'total_cost': 'sum',
    'id': 'count'
}).round(2).sort_values(
    'total_tokens',
    ascending=False
).head(10)

top_users.columns = [
    'Total Tokens',
    'Total Cost ($)',
    'API Calls'
]

# Convert index to regular column
top_users = top_users.reset_index()

# Rename username
top_users = top_users.rename(
    columns={'username': 'Username'}
)

# Display as HTML dark table
st.markdown(
    top_users.to_html(
        index=False,
        classes='dark-table',
        escape=False
    ),
    unsafe_allow_html=True
)
 
# --- Row 6: Detailed Data Table ---
st.subheader("📋 Usage Log")

display_columns = [
    'created_at',
    'username',
    'usage_type',
    'model',
    'input_tokens',
    'output_tokens',
    'total_tokens',
    'total_cost',
    'status',
    'error_message'
]

available_columns = [
    col for col in display_columns
    if col in filtered_df.columns
]

usage_log = filtered_df[
    available_columns
].sort_values(
    'created_at',
    ascending=False
)
num_logs = st.selectbox(
    "Number of recent logs to display",
    [10, 20, 50, 100],
    index=0
)

# Display only the latest selected number of logs
usage_log = usage_log.head(num_logs)

# Rename columns
usage_log = usage_log.rename(columns={
    'created_at': 'Created At',
    'username': 'Username',
    'usage_type': 'Usage Type',
    'model': 'Model',
    'input_tokens': 'Input Tokens',
    'output_tokens': 'Output Tokens',
    'total_tokens': 'Total Tokens',
    'total_cost': 'Total Cost',
    'status': 'Status',
    'error_message': 'Error Message'
})

# Display as HTML dark table
st.markdown(
    usage_log.to_html(
        index=False,
        classes='dark-table',
        escape=False
    ),
    unsafe_allow_html=True
)
 
# --- Download Button ---
st.subheader("📥 Export Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name=f"llm_usage_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)
 
# --- Footer ---
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: gray;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>",
    unsafe_allow_html=True
)
 