import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(page_title="RSI Monitor", page_icon="📈", layout="wide")

st.title("📈 RSI Monitor – testowa wersja bez błędów składni")
st.write("Sprawdza RSI (14) dla wybranych aktywów w interwałach H1 i D1.")

def get_rsi(symbol, interval):
    data = yf.download(symbol, period="14d", interval=interval, progress=False)
    if data.empty or "Close" not in data.columns:
        return None
    data["RSI"] = RSIIndicator(data["Close"], window=14).rsi()
    return round(data["RSI"].iloc[-1], 1)

def rsi_status(val):
    if val is None:
        return "⚠️ brak danych"
    if val > 65:
        return "🔴 wykupienie"
    elif val < 35:
        return "🟢 wyprzedanie"
    return "⚪ neutralne"

symbols = ["EURUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD"]

if st.button("🔍 Sprawdź RSI teraz"):
    results = []
    for s in symbols:
        try:
            rsi_h1 = get_rsi(s, "1h")
            rsi_d1 = get_rsi(s, "1d")
            stat_h1 = rsi_status(rsi_h1)
            stat_d1 = rsi_status(rsi_d1)
            confirm = "✅ TAK" if stat_h1 == stat_d1 and "neutralne" not in stat_h1 else "❌ NIE"
            results.append({
                "Symbol": s,
                "RSI_H1": rsi_h1,
                "Status_H1": stat_h1,
                "RSI_D1": rsi_d1,
                "Status_D1": stat_d1,
                "Potwierdzenie": confirm
            })
        except Exception as e:
            results.append({
                "Symbol": s,
                "RSI_H1": "-",
                "Status_H1": f"Błąd: {e}",
                "RSI_D1": "-",
                "Status_D1": "-",
                "Potwierdzenie": "❌"
            })
    st.dataframe(pd.DataFrame(results), use_container_width=True)

st.caption("Działa lokalnie i w chmurze • Dane: Yahoo Finance • Brak automatycznych pętli i maili.")
