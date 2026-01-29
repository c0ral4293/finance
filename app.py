import streamlit as st
from ratios import calculate_ratios

st.set_page_config(page_title="Financial Ratio Analyzer", layout="centered")

st.title("📊 Financial Ratio Analyzer")

ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, TSLA (use .NS for indian companies)):")

if ticker:
    try:
        df = calculate_ratios(ticker.upper())
        st.success("Data fetched successfully")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")