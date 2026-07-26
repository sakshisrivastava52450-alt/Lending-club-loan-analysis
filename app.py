import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Lending Club Loan Analysis",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Lending Club Loan Analysis Dashboard")
st.markdown("Analyze Lending Club loan data using Python and Streamlit.")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("loan.csv", low_memory=False)
# Convert Interest Rate to numeric
df["int_rate"] = (
    df["int_rate"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["int_rate"] = pd.to_numeric(df["int_rate"], errors="coerce")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

grade = st.sidebar.multiselect(
    "Select Grade",
    options=df["grade"].dropna().unique(),
    default=df["grade"].dropna().unique()
)

status = st.sidebar.multiselect(
    "Select Loan Status",
    options=df["loan_status"].dropna().unique(),
    default=df["loan_status"].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df["grade"].isin(grade)) &
    (df["loan_status"].isin(status))
]

# -----------------------------
# KPI Cards
# -----------------------------
total_loans = len(filtered_df)
funded = filtered_df["loan_amnt"].sum()
avg_loan = filtered_df["loan_amnt"].mean()
filtered_df["int_rate"] = (
    filtered_df["int_rate"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

filtered_df["int_rate"] = pd.to_numeric(
    filtered_df["int_rate"],
    errors="coerce"
)
avg_interest = 0

col1, col2, col3, col4 = st.columns(4)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background-color:#4CAF50;
                padding:20px;
                border-radius:12px;
                text-align:center;
                color:white;'>
        <h4>Total Loans</h4>
        <h2>{:,}</h2>
    </div>
    """.format(total_loans), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color:#2196F3;
                padding:20px;
                border-radius:12px;
                text-align:center;
                color:white;'>
        <h4>Funded Amount</h4>
        <h2>${:,.0f}</h2>
    </div>
    """.format(funded), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color:#FF9800;
                padding:20px;
                border-radius:12px;
                text-align:center;
                color:white;'>
        <h4>Average Loan</h4>
        <h2>${:,.0f}</h2>
    </div>
    """.format(avg_loan), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background-color:#E91E63;
                padding:20px;
                border-radius:12px;
                text-align:center;
                color:white;'>
        <h4>Average Interest</h4>
        <h2>{:.2f}%</h2>
    </div>
    """.format(avg_interest), unsafe_allow_html=True)
st.markdown("---")
st.subheader("📊 Loan Status Distribution")

loan_status = filtered_df["loan_status"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))
loan_status.plot(kind="bar", ax=ax)
ax.set_xlabel("Loan Status")
ax.set_ylabel("Count")

st.pyplot(fig)
st.subheader("📈 Loan Grade")

grade = filtered_df["grade"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))
grade.plot(kind="bar", ax=ax)

st.pyplot(fig)
st.subheader("💰 Loan Purpose")

purpose = filtered_df["purpose"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8,4))
purpose.plot(kind="barh", ax=ax)

st.pyplot(fig)
st.subheader("📉 Interest Rate Distribution")

fig, ax = plt.subplots(figsize=(7,4))

filtered_df["int_rate"].hist(ax=ax)

st.pyplot(fig)
st.subheader("💵 Loan Amount Distribution")

fig, ax = plt.subplots(figsize=(7,4))

filtered_df["loan_amnt"].hist(ax=ax)

st.pyplot(fig)
st.subheader("Loan Amount vs Annual Income")

fig, ax = plt.subplots(figsize=(7,5))

ax.scatter(
    filtered_df["annual_inc"],
    filtered_df["loan_amnt"]
)

ax.set_xlabel("Annual Income")
ax.set_ylabel("Loan Amount")

st.pyplot(fig)
