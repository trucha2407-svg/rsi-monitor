import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="RSI Monitor", page_icon="📈", layout="wide")
st.title("📈 RSI Monitor – analiza RSI (H1 + D1)")
st.write("Progi: RSI > 65 → 🔴 wykupienie, RSI < 35 → 🟢 wyprzedanie")

# --- FUNKCJE ---
def get_rsi(symbol, interval):
    data = yf.download(symbol, period="14d", interval=interval, progress=False)
    if data.empty or "Close" not in data.columns:
        return None
    data["RSI"] = RSIIndicator(data["Close"], window=14).rsi()
    return round(data["RSI"].iloc[-1], 1)

def rsi_status(val):
    if val is None:
        return "⚠️ brak danych"
    if val >
