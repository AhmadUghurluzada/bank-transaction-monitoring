import streamlit as st 
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Bank Transaction Monitoring Dashboard", 
    layout="wide"
)

st.title("Bank Transaction Monitoring Dashboard")


#load processed datasets produced by ETL pipeline
@st.cache_data
def load_data():
    customers_df = pd.read_csv("data/processed/CSVs/customers.csv")
    accounts_df = pd.read_csv("data/processed/CSVs/accounts.csv")
    transactions_df = pd.read_csv("data/processed/CSVs/transactions.csv")
    flags_df = pd.read_csv("data/processed/CSVs/transaction_flags.csv")
    return customers_df, accounts_df, transactions_df, flags_df

customers_df, accounts_df, transactions_df, flags_df = load_data()


# Display key metrics
st.subheader("Data Overview")

total_transactions = len(transactions_df)
total_amount = transactions_df["amount"].sum()
flagged_transactions = flags_df["transaction_id"].nunique()
flag_ratio = (flagged_transactions / total_transactions) * 100


# Display KPIs in a single row
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Amount Transacted", f"${total_amount:,.2f}")
col3.metric("Flagged Transactions", flagged_transactions)
col4.metric("Flagged Transaction Ratio (%)", f"{flag_ratio:.2f}%")


st.subheader("Transaction Activity Over Time")

# Extract hour from timestamp
transactions_df["hour"] = pd.to_datetime(transactions_df["timestamp"]).dt.hour

# Count number of transactions per hour
txn_per_hour = (
    transactions_df
    .groupby("hour")
    .size()
    .reset_index(name="transaction_count")
)

# Line chart of transactions per hour
fig = px.line(
    txn_per_hour,
    x="hour",
    y="transaction_count",
    title="Transactions per Hour"
)

st.plotly_chart(fig, use_container_width=True)



st.subheader("Flags by Type")

# Aggregate flags by type
flags_by_type = (
    flags_df
    .groupby("flag_type")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

fig = px.bar(
    flags_by_type,
    x="flag_type",
    y="count",
    title="Flags by Type"
)

st.plotly_chart(fig, use_container_width=True)



st.subheader("Flags by Customer Risk Rating")

# Enrich flags with customer risk ratings
flags_enriched = (
    flags_df
    .merge(transactions_df[["transaction_id", "account_id"]], on="transaction_id")
    .merge(accounts_df[["account_id", "customer_id"]], on="account_id")
    .merge(customers_df[["customer_id", "risk_rating"]], on="customer_id")
)

# Aggregate flags by customer risk rating
risk_flags = (
    flags_enriched
    .groupby("risk_rating")
    .size()
    .reset_index(name="flag_count")
)

fig = px.bar(
    risk_flags,
    x="risk_rating",
    y="flag_count",
    title="Flags by Customer Risk Rating"
)

st.plotly_chart(fig, use_container_width=True)



st.subheader("Top Customers by Transaction Volume")

# Aggregate transaction amounts by customer
customer_volume = (
    transactions_df
    .merge(accounts_df[["account_id", "customer_id"]], on="account_id")
    .groupby("customer_id")["amount"]
    .sum()
    .reset_index()
    .sort_values("amount", ascending=False)
    .head(10)
)

fig = px.bar(
    customer_volume,
    x="customer_id",
    y="amount",
    title="Top 10 Customers by Transaction Amount"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Flagged Transactions Detail")

# Create detailed table with customer context
flagged_table = (
    flags_df
    .merge(transactions_df, on="transaction_id")
    .merge(accounts_df[["account_id", "customer_id"]], on="account_id")
)

# Display most recent flagged transactions
st.dataframe(
    flagged_table.sort_values("timestamp", ascending=False),
    use_container_width=True
)


