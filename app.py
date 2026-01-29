import streamlit as st

st.title("📊 Financial Ratios Analyzer - Debug Mode")

# Test 1: Check if we can import basic libraries
try:
    import pandas as pd
    import numpy as np
    import yfinance as yf
    st.success("✅ All basic libraries imported successfully")
except Exception as e:
    st.error(f"❌ Library import failed: {e}")
    st.stop()

# Test 2: Try to import ratios.py
try:
    from ratios import calculate_ratios
    st.success("✅ ratios.py imported successfully")
except Exception as e:
    st.error(f"❌ Failed to import ratios.py: {e}")
    st.write("Full error:")
    st.exception(e)
    st.stop()

# Test 3: Try to run the function
ticker_symbol = st.text_input("Enter Stock Ticker", value="AAPL").upper()

if st.button("Analyze"):
    try:
        with st.spinner("Fetching data..."):
            df = calculate_ratios(ticker_symbol)
        st.success("✅ Function executed successfully")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Function failed: {e}")
        st.exception(e)