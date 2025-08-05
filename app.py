import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 AI Momentum Stock Scanner")

tickers = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'TSLA', 'META', 'GOOGL']

def get_momentum_stocks(tickers):
    results = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="20d", interval="1d")
            if df.empty or 'Close' not in df.columns:
                continue  # skip invalid or empty tickers

            # Defensive coding: ensure we have at least 6 days of data
            if len(df) < 6:
                continue

            price_change = (df['Close'][-1] - df['Close'][-6]) / df['Close'][-6]
            volume_avg = df['Volume'][-20:].mean()
            volume_ratio = df['Volume'][-1] / volume_avg

            if price_change > 0.05 and volume_ratio > 1.5:
                results.append({
                    'Ticker': ticker,
                    '5d % Change': round(price_change * 100, 2),
                    'Volume Spike': round(volume_ratio, 2)
                })
        except Exception as e:
            st.write(f"Error with {ticker}: {e}")
            continue

    return pd.DataFrame(results)
