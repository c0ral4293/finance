import streamlit as st
import pandas as pd
from ratios import calculate_ratios

st.set_page_config(
    page_title="Financial Ratio Analyzer",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Financial Ratio Analyzer")

ticker = st.text_input(
    "Enter stock ticker (e.g. AAPL, MSFT, TSLA):",
    value=""
)

if ticker:
    try:
        with st.spinner("Fetching financial data..."):
            df = calculate_ratios(ticker.upper())

        st.subheader("Financial Ratios (2025 vs 2024)")
        st.dataframe(
            df.style.format("{:.2f}"),
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error fetching data: {e}")
