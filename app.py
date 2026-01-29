import streamlit as st
from ratios import calculate_ratios

st.set_page_config(page_title="Financial Ratio Analyzer", layout="wide")

st.title("📊 Financial Ratio Analyzer")

ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, TSLA):")

if ticker:
    try:
        with st.spinner("Fetching financial data..."):
            df = calculate_ratios(ticker.upper())

        st.subheader("📈 Financial Ratios")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")