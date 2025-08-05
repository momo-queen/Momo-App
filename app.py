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

            if df is None or df.empty or 'Close' not in df.columns or 'Volume' not in df.columns:
                st.warning(f"{ticker} returned no usable data.")
                continue
            if df['Close'].isna().any() or df['Volume'].isna().any():
                st.warning(f"{ticker} has missing Close or Volume values.")
                continue
            if len(df) < 6:
                st.warning(f"{ticker} has less than 6 days of data.")
                continue

            price_change = (df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6]
            volume_avg = df['Volume'].tail(20).mean()
            volume_ratio = df['Volume'].iloc[-1] / volume_avg if volume_avg else 0

            if price_change > 0.05 and volume_ratio > 1.5:
                results.append({
                    'Ticker': ticker,
                    '5d % Change': round(price_change * 100, 2),
                    'Volume Spike': round(volume_ratio, 2)
                })

        except Exception as e:
            st.error(f"Error with {ticker}: {e}")
            continue

    return pd.DataFrame(results)

if st.button("🔍 Run Scanner"):
    with st.spinner("Scanning tickers..."):
        df = get_momentum_stocks(tickers)

    if df.empty:
        st.info("No momentum stocks found.")
    else:
        st.success(f"Found {len(df)} stock(s) with momentum!")
        st.dataframe(df)
