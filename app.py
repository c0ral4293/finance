import streamlit as st
from ratios import fetch_data, calculate_ratios

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Financial Ratio Analyzer",
    layout="centered"
)

st.title("📊 Financial Ratio Analyzer (2025 vs 2024)")

# -------------------------------
# User input
# -------------------------------
ticker = st.text_input(
    "Enter stock ticker (e.g. AAPL, MSFT):",
    placeholder="AAPL"
)

# -------------------------------
# Cached data fetch + calculation
# -------------------------------
@st.cache_data(ttl=3600)
def get_ratios(ticker):
    info, financials, balance_sheet = fetch_data(ticker)
    return calculate_ratios(info, financials, balance_sheet)

# -------------------------------
# App logic
# -------------------------------
if ticker:
    with st.spinner("Fetching financial data..."):
        df = get_ratios(ticker.upper())

    if not df.empty:
        st.subheader("📈 Financial Ratios")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("No financial data available for this ticker.")