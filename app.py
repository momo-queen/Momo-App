
import yfinance as yf
import pandas as pd

st.title("📈 AI Momentum Stock Scanner")

tickers = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'TSLA', 'META', 'GOOGL']

def get_momentum_stocks(tickers):
    results = []
    for ticker in tickers:
        df = yf.download(ticker, period="20d", interval="1d")
        if len(df) < 10:
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
    return pd.DataFrame(results)

if st.button("Run Scanner"):
    df = get_momentum_stocks(tickers)
    if df.empty:
        st.write("No momentum stocks found today.")
    else:
        st.dataframe(df)
