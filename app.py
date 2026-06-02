import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# PAGE SETTINGS
st.set_page_config(
    page_title="The Investor Mama",
    layout="wide"
)

# TITLE
st.title("The Investor Mama")
st.subheader("Portfolio Analytics Dashboard")

st.write("Track portfolio performance and stock allocation.")

# SAMPLE PORTFOLIO
portfolio = {
    "Ticker": ["AAPL", "MSFT", "NVDA", "TSLA"],
    "Shares": [10, 5, 3, 7]
}

df = pd.DataFrame(portfolio)

# GET LIVE STOCK PRICES
prices = []

for ticker in df["Ticker"]:
    stock = yf.Ticker(ticker)
    latest_price = stock.history(period="1d")["Close"].iloc[-1]
    prices.append(latest_price)

df["Price"] = prices

# CALCULATE VALUE
df["Value"] = df["Shares"] * df["Price"]

# TOTAL PORTFOLIO VALUE
total_value = df["Value"].sum()

# KPI CARDS
col1, col2 = st.columns(2)

col1.metric(
    "Total Portfolio Value",
    f"${total_value:,.2f}"
)

col2.metric(
    "Number of Holdings",
    len(df)
)

# TABLE
st.subheader("Portfolio Holdings")
st.dataframe(df)

# PIE CHART
st.subheader("Portfolio Allocation")

fig = px.pie(
    df,
    names="Ticker",
    values="Value",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)
