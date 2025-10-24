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
        return "⚠️ brak danych"
    if value > 65:
        return "🔴 wykupienie"
    elif value < 35:
        return "🟢 wyprzedanie"
    else:
        return "⚪ neutralne"

# --- INTERFEJS ---
st.set_page_config(page_title="RSI Monitor", page_icon="📈", layout="wide")
st.title("📈 RSI Monitor – szybka analiza RSI (H1 + D1)")
st.markdown("Progi: **RSI > 65 → wykupienie**, **RSI < 35 → wyprzedanie**")

symbols = ["EURUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD", "XAUUSD=X", "CL=F"]

if st.button("🔍 Sprawdź RSI teraz"):
    results = []
    for sym in symbols:
        try:
            rsi_h1 = get_rsi(sym, "1h")
            rsi_d1 = get_rsi(sym, "1d")
            stat_h1 = rsi_status(rsi_h1)
            stat_d1 = rsi_status(rsi_d1)
            confirm = "✅ TAK" if (
                rsi_h1 is not None and
                rsi_d1 is not None and
                stat_h1 == stat_d1 and
                "neutralne" not in stat_h1
            ) else "❌ NIE"

            results.append({
                "Symbol": sym,
                "RSI_H1": rsi_h1 if rsi_h1 is not None else "-",
                "Status_H1": stat_h1,
                "RSI_D1": rsi_d1 if rsi_d1 is not None else "-",
                "Status_D1": stat_d1,
                "Potwierdzenie (H1+D1)": confirm
            })
        except Exception as e:
            results.append({
                "Symbol": sym,
                "RSI_H1": "-",
                "Status_H1": f"❌ Błąd: {e}",
                "RSI_D1": "-",
                "Status_D1": "-",
                "Potwierdzenie (H1+D1)": "❌"
            })

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

st.caption("Działa lokalnie i w chmurze • Dane: Yahoo Finance • Brak automatycznych pętli i maili.")
