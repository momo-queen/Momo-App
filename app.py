import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 AI Momentum Stock Scanner")

tickers = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'TSLA', 'META', 'GOOGL','OSS','RGTI','IONQ','INOD','SMCI']

def get_momentum_stocks(tickers):
    results = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="20d", interval="1d")
            
            # Validate required data
            if df.empty:
                st.warning(f"{ticker} returned no data.")
                continue
            if 'Close' not in df.columns or 'Volume' not in df.columns:
                st.warning(f"{ticker} is missing required data columns.")
                continue
            if len(df) < 6:
                st.warning(f"{ticker} has less than 6 trading days of data.")
                continue
            if df['Close'].isna().sum() > 0 or df['Volume'].isna().sum() > 0:
                st.warning(f"{ticker} has missing Close or Volume values.")
                continue

            # Momentum logic
            price_change = (df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6]
            volume_avg = df['Volume'][-20:].mean()
            volume_ratio = df['Volume'].iloc[-1] / volume_avg

            if price_change > 0.05 and volume_ratio > 1.5:
                results.append({
                    'Ticker': ticker,
                    '5d % Change': round(price_change * 100, 2),
                    'Volume Spike': round(volume_ratio, 2)
                })

        except Exception as e:
            st.error(f"Error with {ticker}: {str(e)}")
            continue

    return pd.DataFrame(results)
