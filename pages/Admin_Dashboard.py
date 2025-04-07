import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Admin":
    st.error("Unauthorized Access! Please log in as Admin.")
    st.stop()

# --- Setup CSV File ---
file_path = "sales_data.csv"

# Load existing sales data
if os.path.exists(file_path):
    sales_data = pd.read_csv(file_path)

    # Ensure CSV has correct columns
    required_columns = ["Date", "Salesperson", "Product", "Quantity Sold", "Amount"]
    for col in required_columns:
        if col not in sales_data.columns:
            sales_data[col] = None  # Add missing columns if they don't exist
else:
    sales_data = pd.DataFrame(columns=["Date", "Salesperson", "Product", "Quantity Sold", "Amount"])


# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# --- CUSTOM CSS FOR A MODERN LOOK ---
st.markdown("""
    <style>
    /* KPI Cards */
    .metric-container { 
        display: flex; 
        justify-content: space-between; 
        gap: 20px; 
        margin-bottom: 20px;
    }
    .kpi-card {
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        text-align: center;
        flex-grow: 1;
    }
    .green { background-color: #28a745; }
    .blue { background-color: #007bff; }
    .red { background-color: #dc3545; }
    .yellow { background-color: #ffc107; color: black; }

    /* Sales History */
    .sales-history {
        margin-top: 20px;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 style='text-align: center;'>📊 Welcome to Admin Dashboard</h1>", unsafe_allow_html=True)

# --- KPI METRICS ---
total_sales = sales_data["Amount"].sum() if not sales_data.empty else 0
transactions = len(sales_data)
# Ensure 'Amount' column is numeric
sales_data["Amount"] = pd.to_numeric(sales_data["Amount"], errors='coerce')

if sales_data.empty or sales_data["Amount"].dropna().empty:
    best_salesperson = "N/A"
else:
    best_salesperson = sales_data.groupby("Salesperson")["Amount"].sum()
    best_salesperson = best_salesperson[best_salesperson > 0]  # Filter out zero sales
    best_salesperson = best_salesperson.idxmax() if not best_salesperson.empty else "N/A"

# Ensure sales_data has the required column before summing
if "Quantity Sold" in sales_data.columns:
    total_units_sold = sales_data["Quantity Sold"].sum()
else:
    total_units_sold = 0  # Default value if column is missing

# --- DISPLAY KPI CARDS ---
st.markdown("<div class='metric-container'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='kpi-card green'>🏅 Total Sales:<br><b>RM {total_sales}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-card blue'>📊 Transactions:<br><b>{transactions}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-card red'>🏆 Top Seller:<br><b>{best_salesperson}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-card yellow'>📦 Units Sold:<br><b>{total_units_sold}</b></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- SALES HISTORY TABLE ---
st.markdown("<div class='sales-history'>📜 Sales History</div>", unsafe_allow_html=True)
st.dataframe(sales_data)

# --- SALES CHARTS & GRAPHS ---
st.markdown("<h2>📊 Sales Insights</h2>", unsafe_allow_html=True)

# --- Interactive Plotly Chart for Total Sales by Salesperson ---
if not sales_data.empty:
    st.markdown("### 💰 Total Sales by Salesperson")

    # Group sales data by Salesperson
    salesperson_sales = sales_data.groupby("Salesperson")["Amount"].sum().reset_index()

    # Create an interactive bar chart with Plotly
    fig = px.bar(
        salesperson_sales,
        x="Amount",
        y="Salesperson",
        orientation="h",
        color="Amount",
        color_continuous_scale="viridis",
        title="💰 Total Sales by Salesperson"
    )

    # Update layout for a modern look
    fig.update_layout(
        xaxis_title="Total Sales (RM)",
        yaxis_title="Salesperson",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Show the chart in Streamlit
    st.plotly_chart(fig)

# --- Interactive Plotly Chart for Total Units Sold by Product ---
if not sales_data.empty:
    st.markdown("### 🛒 Total Units Sold per Product")

    # Group sales data by Product
    product_sales = sales_data.groupby("Product")["Quantity Sold"].sum().reset_index()

    # Create an interactive bar chart with Plotly
    fig = px.bar(
        product_sales,
        x="Quantity Sold",
        y="Product",
        orientation="h",
        color="Quantity Sold",
        color_continuous_scale="magma",
        title="🛒 Total Units Sold per Product"
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Total Units Sold",
        yaxis_title="Product",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Show the chart
    st.plotly_chart(fig)

# --- Interactive Sales Trend Over Time Chart ---
if not sales_data.empty:
    st.markdown("### 📈 Sales Trend Over Time")

    # Ensure date format
    sales_data["Date"] = pd.to_datetime(sales_data["Date"])
    sales_trend = sales_data.groupby("Date")["Amount"].sum().reset_index()

    # Create an interactive line chart
    fig = px.line(
        sales_trend,
        x="Date",
        y="Amount",
        markers=True,
        title="📈 Sales Trend Over Time"
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales (RM)",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Show the chart
    st.plotly_chart(fig)
