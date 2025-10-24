import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

# --- FUNKCJE ---
def get_rsi(symbol, interval):
    data = yf.download(symbol, period="14d", interval=interval, progress=False)
    if data.empty or "Close" not in data.columns:
        return None
    data["RSI"] = RSIIndicator(data["Close"], window=14).rsi()
    return round(data["RSI"].iloc[-1], 1)

def rsi_status(value):
    if value is None:
        return "⚠️ brak danych", "#ffffff"
    if value > 65:
        return "🔴 wykupienie", "#ffcccc"
    elif value < 35:
        return "🟢 wyprzedanie", "#ccffcc"
    else:
        return "⚪ neutralne", "#f0f0f0"

# --- INTERFEJS ---
st.set_page_config(page_title="RSI Monitor", page_icon="📈", layout="wide")
st.title("📈 RSI Monitor – szybka analiza RSI (H1 + D1)")
st.markdown("Progi: **RSI > 65 → wykupienie**, **RSI < 35 → wyprzedanie**")

symbols = ["EURUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD", "XAUUSD=X", "CL=F"]

if st.button("🔍 Sprawdź RSI teraz"):
    rows = []
    for sym in symbols:
        try:
            rsi_h1 = get_rsi(sym, "1h")
            rsi_d1 = get_rsi(sym, "1d")
            stat_h1, color_h1 = rsi_status(rsi_h1)
            stat_d1, color_d1 = rsi_status(rsi_d1)
            confirm = "✅ TAK" if (
                rsi_h1 is not None and
                rsi_d1 is not None and
                stat_h1 == stat_d1 and
                "neutralne" not in stat_h1
            ) else "❌ NIE"

            rows.append({
                "Symbol": sym,
                "RSI_H1": rsi_h1 if rsi_h1 is not None else "-",
                "Status_H1": stat_h1,
                "Kolor_H1": color_h1,
