import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Momentum Scanner", layout="centered")
st.title("📈 AI Momentum Stock Scanner")

tickers = ['AAPL', 'SMCI', 'NVDA', 'AMZN', 'TSLA']

def get_momentum_stocks(tickers):
    results = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="20d", interval="1d", threads=False)

            if df.empty or 'Close' not in df.columns or 'Volume' not in df.columns:
                st.warning(f"{ticker} returned no usable data.")
                continue
            if df['Close'].isna().sum() > 0 or df['Volume'].isna().sum() > 0:
                st.warning(f"{ticker} has missing values.")
                continue
            if len(df) < 6:
                st.warning(f"{ticker} has less than 6 days of data.")
                continue

            price_change = (df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6]
            volume_avg = df['Volume'][-20:].mean()
            volume_ratio = df['Volume'].iloc[-1] / volume_avg

            if price_change >_
