import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(page_title="RSI Monitor", page_icon="📈")
st.title("📈 RSI Monitor – poprawiona wersja (stabilna)")
st.write("Progi: RSI > 65 → 🔴 wykupienie, RSI < 35 → 🟢 wyprzedanie")

# --- FUNKCJE ---
def get_rsi(symbol, interval):
    data = yf.download(symbol, period="14d", interval=interval, progress=False)
    # zabezpieczenie: brak danych
    if data is None or data.empty:
        return None
    # jeśli kolumny mają złożony indeks (MultiIndex)
    if isinstance(data.columns, pd.MultiIndex):
        # próbuj wziąć poziom 'Close' jeśli istnieje
        try:
            data = data["Close"]
        except Exception:
            return None
    # jeśli to DataFrame, weź pierwszą kolumnę Close
    if isinstance(data, pd.DataFrame):
        if "Close" in data.columns:
            data = data["Close"]
        else:
            # jeśli już to Series, zostaw
            if not isinstance(data, pd.Series):
                return None
    # po tym punkcie mamy Series z wartościami Close
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
        r1 = get_rsi(s, "1h")
        r2 = get_rsi(s, "1d")
        st1 = rsi_status(r1)
        st2 = rsi_status(r2)
        conf = "✅ TAK" if r1 and r2 and st1 == st2 and "neutralne" not in st1 else "❌ NIE"
        out.append({
            "Symbol": s,
            "RSI_H1": r1 if r1 is not None else "-",
            "Status_H1": st1,
            "RSI_D1": r2 if r2 is not None else "-",
            "Status_D1": st2,
            "Potwierdzenie": conf
        })
    st.dataframe(pd.DataFrame(out), use_container_width=True)

st.caption("Działa w chmurze • Dane z Yahoo Finance • RSI(14) • Progi 35/65")
