import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portfolio Dashboard")

st.title("📊 Portfolio Dashboard")

st.sidebar.header("Portfolio Input")

tickers = st.sidebar.text_input(
    "Enter tickers (comma separated)",
    "AAPL,MSFT,NVDA,TSLA"
)

shares = st.sidebar.text_input(
    "Enter shares (comma separated)",
    "10,5,3,7"
)

# Safe cleaning
ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
share_list_raw = [s.strip() for s in shares.split(",") if s.strip()]

# Validation
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

st.dataframe(df)
