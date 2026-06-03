import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="The Investor Mama", layout="wide")

st.title("The Investor Mama")
st.subheader("Portfolio Analytics Dashboard")

st.sidebar.header("Portfolio Input")

tickers = st.sidebar.text_input(
    "Enter tickers (comma separated)",
    "AAPL,MSFT,NVDA,TSLA"
)

shares = st.sidebar.text_input(
    "Enter shares (comma separated)",
    "10,5,3,7"
)

ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
share_list_raw = [s.strip() for s in shares.split(",") if s.strip()]

if len(ticker_list) != len(share_list_raw):
    st.sidebar.error("Tickers and shares must match")
    st.stop()

try:
    share_list = [int(s) for s in share_list_raw]
except:
    st.sidebar.error("Shares must be valid numbers only")
    st.stop()

df = pd.DataFrame({
    "Ticker": ticker_list,
    "Shares": share_list
})

prices = []

for ticker in df["Ticker"]:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")

    if data.empty:
        st.error(f"No price data found for {ticker}")
        st.stop()

    latest_price = data["Close"].iloc[-1]
    prices.append(latest_price)

df["Price"] = prices
df["Value"] = df["Shares"] * df["Price"]

total_value = df["Value"].sum()

col1, col2 = st.columns(2)

col1.metric("Total Portfolio Value", f"${total_value:,.2f}")
col2.metric("Number of Holdings", len(df))

st.subheader("Portfolio Holdings")
st.dataframe(df)

st.subheader("Portfolio Allocation")

fig = px.pie(
    df,
    names="Ticker",
    values="Value",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)
