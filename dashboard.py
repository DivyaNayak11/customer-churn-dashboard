#------IMPORT LIBRARIES------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#------PAGE CONGIF------
st.set_page_config(
    page_title="European Bank Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

#------LOAD DATA------
@st.cache_data
def load_data():
    df = pd.read_csv(r"European_churn_cleaned.csv")
    return df
df = load_data()

#------SIDEBAR FILTERS------
st.sidebar.header("Dashboard Filters")

geo_filter = st.sidebar.multiselect(
    "Select Geography",
    options=df['GeographySegment'].unique(),
    default=df['GeographySegment'].unique()
)

age_filter = st.sidebar.multiselect(
    "Select Age Group",
    options=df['AgeGroup'].unique(),
    default=df['AgeGroup'].unique()
)

cr_score_filter = st.sidebar.multiselect(
    "Select Credit Score",
    options=df['CreditScoreSegment'].unique(),
    default=df['CreditScoreSegment'].unique()
)

tenure_filter = st.sidebar.multiselect(
    "Select Tenure Group",
    options=df['TenureGroup'].unique(),
    default=df['TenureGroup'].unique()
)

balance_filter = st.sidebar.multiselect(
    "Select Balance",
    options=df['BalanceSegment'].unique(),
    default=df['BalanceSegment'].unique()
)

#apply filters
filtered_df = df[
    (df['GeographySegment'].isin(geo_filter)) &
    (df['AgeGroup'].isin(age_filter)) &
    (df['CreditScoreSegment'].isin(cr_score_filter)) &
    (df['TenureGroup'].isin(tenure_filter)) &
    (df['BalanceSegment'].isin(balance_filter))
]

#------DASHBOARD TITLE------
st.title("📊 Customer Segmentation & Churn Pattern Analytics in European Banking Dashboard")

#------KPI CALCULATIONS------
total_customers = filtered_df.shape[0]

overall_churn_rate = (
    filtered_df['Exited'].mean() * 100
)

premium_customers = filtered_df[
    filtered_df['Balance'] > filtered_df['Balance'].median()
]

inactive_customers = filtered_df[
    filtered_df['IsActiveMember'] == 0
]

high_value_churn_ratio = (
    premium_customers['Exited'].mean() * 100
)

geo_risk = filtered_df.groupby(
    'GeographySegment'
)['Exited'].mean().max() * 100

engagement_drop = (
    inactive_customers['Exited'].mean() * 100
)

#------KPI SECTION------
st.subheader("Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Overall Churn Rate",
        value=f"{overall_churn_rate:.2f}%"
    )
    st.caption("Percentage of customers who exited")

with kpi2:
    st.metric(
        label="High-Value Churn Ratio",
        value=f"{high_value_churn_ratio:.2f}%"
    )
    st.caption("Churn among premium customers")

with kpi3:
    st.metric(
        label="Geographic Risk Index",
        value=f"{geo_risk:.2f}%"
    )
    st.caption("Highest regional churn exposure")

with kpi4:
    st.metric(
        label="Engagement Drop Indicator",
        value=f"{engagement_drop:.2f}%"
    )
    st.caption("Inactive customer churn risk")

#------ROW 1 VISUALS------
col1, col2 = st.columns(2)

#geography-wise churn
with col1:
    geo_churn = filtered_df.groupby(
        'GeographySegment'
    )['Exited'].mean().reset_index()

    fig_geo = px.bar(
        geo_churn,
        x='GeographySegment',
        y='Exited',
        color='GeographySegment',
        title="Geography-wise Churn Rate",
        text_auto='.2%'
    )
    fig_geo.update_layout(
        yaxis_title="Churn Rate",
        xaxis_title="Region"
    )
    st.plotly_chart(fig_geo, use_container_width=True)

#age churn comparison
with col2:
    age_churn = filtered_df.groupby(
        'AgeGroup'
    )['Exited'].mean().reset_index()

    fig_age = px.line(
        age_churn,
        x='AgeGroup',
        y='Exited',
        markers=True,
        title="Age Group vs Churn"
    )

    fig_age.update_layout(
        yaxis_title="Churn Rate"
    )
    st.plotly_chart(fig_age, use_container_width=True)

#------ROW 2 VISUALS------
col3, col4 = st.columns(2)

#tenure comparison
with col3:
    tenure_churn = filtered_df.groupby(
        'TenureGroup'
    )['Exited'].mean().reset_index()

    fig_tenure = px.bar(
        tenure_churn,
        x='TenureGroup',
        y='Exited',
        color='TenureGroup',
        title="Tenure vs Churn Rate",
        text_auto='.2%'
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

#high value customer explorer
with col4:
    high_value = filtered_df[
        filtered_df['Balance'] > filtered_df['Balance'].median()
    ]

    fig_high = px.scatter(
        high_value,
        x='Balance',
        y='EstimatedSalary',
        color='Exited',
        size='CreditScore',
        hover_data=['Age', 'GeographySegment'],
        title="High-Value Customer Churn Explorer"
    )
    st.plotly_chart(fig_high, use_container_width=True)

#------SEGMENT CHURN TABLE------
st.subheader("Segment Churn Rate Analysis")

segment_table = filtered_df.groupby(
    ['GeographySegment', 'Gender_Male']
)['Exited'].mean().reset_index()

segment_table['Exited'] = (
    segment_table['Exited'] * 100
).round(2)

segment_table.columns = [
    'GeographySegment',
    'Gender_Male',
    'Churn Rate (%)'
]

st.dataframe(
    segment_table,
    use_container_width=True
)

#------DRILL DOWN SECTION------
st.subheader("Drill-Down Customer View")

churn_filter = st.selectbox(
    "Select Customer Status",
    ["All", "Churned", "Retained"]
)

if churn_filter == "Churned":
    drill_df = filtered_df[filtered_df['Exited'] == 1]
elif churn_filter == "Retained":
    drill_df = filtered_df[filtered_df['Exited'] == 0]
else:
    drill_df = filtered_df

st.dataframe(
    drill_df.head(100),
    use_container_width=True
)

#------FOOTER------
st.markdown("---")
st.markdown("Developed using Streamlit & Plotly for Customer Churn Analytics")