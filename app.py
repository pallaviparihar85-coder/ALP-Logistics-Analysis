import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Title
st.title("📦 ALP Logistics Analysis Dashboard")
st.write("Welcome to my Business Analyst Project!")

# Read Dataset
df = pd.read_csv("APL_Logistics.csv", encoding="latin1")

# Dataset Preview
st.subheader("➤ Dataset Preview")
st.dataframe(df.head())

# Dataset Information
st.subheader("➤ Dataset Information")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

# Statistical Summary
st.subheader("➤ Statistical Summary")
st.dataframe(df.describe())

# Sidebar Filters

st.sidebar.header("➤ Filter Dashboard")

# Market Filter
market = st.sidebar.selectbox(
    "Select Market",
    ["All"] + sorted(df["Market"].dropna().unique())
)

# Order Region Filter
region = st.sidebar.selectbox(
    "Select Order Region",
    ["All"] + sorted(df["Order Region"].dropna().unique())
)

# Customer Segment Filter
segment = st.sidebar.selectbox(
    "Select Customer Segment",
    ["All"] + sorted(df["Customer Segment"].dropna().unique())
)

# Category Filter
category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category Name"].dropna().unique())
)

# Product Filter
product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + sorted(df["Product Name"].dropna().unique())
)

# Discount Rate Slider
discount_range = st.sidebar.slider(
    "Discount Rate",
    min_value=float(df["Order Item Discount Rate"].min()),
    max_value=float(df["Order Item Discount Rate"].max()),
    value=(
        float(df["Order Item Discount Rate"].min()),
        float(df["Order Item Discount Rate"].max())
    )
)

# Apply Filters

filtered_df = df.copy()

if market != "All":
    filtered_df = filtered_df[
        filtered_df["Market"] == market
    ]

if region != "All":
    filtered_df = filtered_df[
        filtered_df["Order Region"] == region
    ]

if segment != "All":
    filtered_df = filtered_df[
        filtered_df["Customer Segment"] == segment
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category Name"] == category
    ]

if product != "All":
    filtered_df = filtered_df[
        filtered_df["Product Name"] == product
    ]

filtered_df = filtered_df[
    (filtered_df["Order Item Discount Rate"] >= discount_range[0]) &
    (filtered_df["Order Item Discount Rate"] <= discount_range[1])
]
# Revenue & Profit Overview

st.header("1.Revenue & Profit Overview")

# KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Order Profit Per Order"].sum()

# KPI Cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="● Total Sales",
        value=f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="● Total Profit",
        value=f"${total_profit:,.2f}"
    )


# Margin Trend Chart

st.subheader("● Margin Trend Chart")

margin_trend = (
    filtered_df.groupby("Market")["Order Item Profit Ratio"]
    .mean()
    .reset_index()
)

fig = px.line(
    margin_trend,
    x="Market",
    y="Order Item Profit Ratio",
    markers=True,
    title="Margin Trend by Market"
)

st.plotly_chart(fig, use_container_width=True)

st.header("2. Customer Value Dashboard")

st.subheader("● Top 10 Customers by Profit")

top_customers = (
    filtered_df.groupby("Customer Id")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="Customer Id",
    y="Order Profit Per Order",
    title="Top 10 Customers by Profit",
    color_discrete_sequence=["darkgreen"]
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("● Bottom 10 Customers by Profit")

bottom_customers = (
    filtered_df.groupby("Customer Id")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=True)
    .head(10)
    .reset_index()
)

fig = px.bar(
    bottom_customers,
    x="Customer Id",
    y="Order Profit Per Order",
    title="Bottom 10 Customers by Profit",
    color_discrete_sequence=["darkred"]
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Segment Contribution")

segment = (
    filtered_df.groupby("Customer Segment")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    segment,
    names="Customer Segment",
    values="Sales",
    title="Customer Segment Contribution"
)

st.plotly_chart(fig, use_container_width=True)

st.header("3.Product & Category Performance")

st.subheader("● Product-level Margin Analysis")

product_margin = (
    filtered_df.groupby("Product Name")["Order Item Profit Ratio"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    product_margin,
    x="Product Name",
    y="Order Item Profit Ratio",
    title="Top 10 Products by Profit Margin"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("● Category Profitability Heatmap")

category_profit = (
    filtered_df.groupby("Category Name")["Order Profit Per Order"]
    .mean()
    .reset_index()
)

pivot = category_profit.pivot_table(
    values="Order Profit Per Order",
    index="Category Name"
)

fig, ax = plt.subplots(figsize=(14,10))

sns.heatmap(
    pivot,
    annot=True,
    cmap="YlGnBu",
    fmt=".2f",
    ax=ax
)

st.pyplot(fig)

st.header("4. Discount Impact Analyzer")

st.subheader("● Discount vs Margin Visualization")

fig = px.scatter(
    filtered_df,
    x="Order Item Discount Rate",
    y="Order Item Profit Ratio",
    title="Discount vs Profit Margin",
    labels={
        "Order Item Discount Rate": "Discount Rate",
        "Order Item Profit Ratio": "Profit Margin"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("What-if Discount Scenario")

discount = st.slider(
    "Select Discount Rate (%)",
    0,
    50,
    10
)

estimated_margin = filtered_df["Order Item Profit Ratio"].mean() * (1 - discount/100)

st.metric(
    "Estimated Profit Margin",
    f"{estimated_margin:.2f}"
)

st.header("➤ Business Insights")

st.markdown("""
- Total sales and profit indicate the overall business performance across different markets.
- A few customers contribute significantly to total profit, while some customers generate low or negative profit.
- Product margin analysis shows that only a limited number of products generate high profitability.
- Category profitability varies across product categories, highlighting the need to focus on high-performing categories.
- Higher discount rates are generally associated with lower profit margins, affecting overall profitability.
""")

st.header("➤ Recommendations")

st.markdown("""
- Focus on retaining high-profit customers through loyalty programs and personalized offers.
- Review products with low profit margins and optimize their pricing strategy.
- Increase investment in high-performing product categories to maximize revenue.
- Avoid excessive discounting on low-margin products to improve profitability.
- Monitor discount strategies regularly to maintain a healthy balance between sales growth and profit margins.
""")

st.header("➤ Conclusion")

st.markdown("""
This dashboard provides a comprehensive analysis of sales, profit, customer value, product performance, and discount impact. The insights help identify profitable customers, products, and categories while highlighting the effect of discounts on business performance. These findings can support data-driven decisions to improve profitability and overall business growth.
""")