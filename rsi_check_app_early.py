import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(page_title="RSI Monitor", page_icon="📈")
st.title("📈 RSI Monitor – prosta wersja")

def get_rsi(symbol, interval):
    data = yf.download(symbol, period="14d", interval=interval, progress=False)
    if data.empty or "Close" not in data.columns:
        return None
    rsi = RSIIndicator(data["Close"], window=14).rsi()
    return round(rsi.iloc[-1], 1)

def rsi_status(v):
    if v is None:
        return "⚠️ brak danych"
    if v > 65:
        return "🔴 wykupienie"
    if v < 35:
        return "🟢 wyprzedanie"
    return "⚪ neutralne"

symbols = ["EURUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD"]

if st.button("🔍 Sprawdź RSI teraz"):
    out = []
    for s in symbols:
        r1 = get_rsi(s, "1h")
        r2 = get_rsi(s, "1d")
        st1 = rsi_status(r1)
        st2 = rsi_status(r2)
        conf = "✅ TAK" if r1 and r2 and st1 == st2 and "neutralne" not in st1 else "❌ NIE"
        out.append({"Symbol": s, "RSI_H1": r1, "Status_H1": st1,
                    "RSI_D1": r2, "Status_D1": st2, "Potwierdzenie": conf})
    st.dataframe(pd.DataFrame(out), use_container_width=True)

st.caption("Działa w chmurze • Dane: Yahoo Finance • RSI(14) • Progi 35/65")
