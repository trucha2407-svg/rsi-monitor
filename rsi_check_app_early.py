import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(page_title="RSI Monitor", page_icon="📈")
st.title("📈 RSI Monitor – uniwersalna wersja")
st.write("Progi: RSI > 65 → 🔴 wykupienie, RSI < 35 → 🟢 wyprzedanie")

def get_rsi(symbol, interval, period="30d"):
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    if data is None or data.empty:
        return None
    if isinstance(data.columns, pd.MultiIndex):
        try:
            data = data["Close"]
        except Exception:
            return None
    if isinstance(data, pd.DataFrame):
        if "Close" in data.columns:
            data = data["Close"]
        else:
            return None
    if data is None or len(data) < 15:
        return None
    try:
        rsi = RSIIndicator(data, window=14).rsi()
        return round(rsi.iloc[-1], 1)
    except Exception:
        return None

def rsi_status(v):
    if v is None:
        return "⚠️ brak danych"
    if v > 65:
        return "🔴 wykupienie"
    if v < 35:
        return "🟢 wyprzedanie"
    return "⚪ neutralne"

symbols = ["EURUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD", "XAUUSD=X", "CL=F"]

if st.button("🔍 Sprawdź RSI teraz"):
    out = []
    for s in symbols:
        # dla kryptowalut pobieramy RSI z H1 i D1
        if "BTC" in s or "ETH" in s:
            rsi_h1 = get_rsi(s, "1h", "7d")
            rsi_d1 = get_rsi(s, "1d", "60d")
        else:
            # dla reszty – tylko D1, H1 pomijamy
            rsi_h1 = None
            rsi_d1 = get_rsi(s, "1d", "60d")

        st1 = rsi_status(rsi_h1)
        st2 = rsi_status(rsi_d1)
        confirm = "✅ TAK" if rsi_h1 and rsi_d1 and st1 == st2 and "neutralne" not in st1 else "❌ NIE"

        out.append({
            "Symbol": s,
            "RSI_H1": rsi_h1 if rsi_h1 is not None else "-",
            "Status_H1": st1,
            "RSI_D1": rsi_d1 if rsi_d1 is not None else "-",
            "Status_D1": st2,
            "Potwierdzenie": confirm
        })
    st.dataframe(pd.DataFrame(out), use_container_width=True)

st.caption("Działa w chmurze • Yahoo Finance ogranicza H1 dla Forex i surowców • RSI(14) • Progi 35/65")
