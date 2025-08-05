import streamlit as st
import yfinance as yf
import pandas as pd

# Set up the app UI
st.set_page_config(page_title="Momentum Scanner", layout="centered")
st.title("📈 AI Momentum Stock Scanner")

# Your initial test ticker list (can expand later)
tickers = ['AAPL', 'SMCI', 'NVDA', 'AMZN', 'TSLA']

# Define the scanning function
def get_momentum_stocks(tickers):
    results = []
    for ticker in tickers:
        try:
            # Download historical data f
