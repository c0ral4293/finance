import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Financial Ratios", page_icon="📊")

st.title("📊 Financial Ratios Analyzer")

# Import check
try:
    from ratios import calculate_ratios
    st.sidebar.success("✅ Backend loaded")
except Exception as e:
    st.error(f"Failed to load ratios module: {e}")
    st.stop()

# Main app
ticker_symbol = st.text_input(
    "Enter Stock Ticker Symbol",
    value="AAPL",
    placeholder="e.g., AAPL, MSFT, GOOGL",
    max_chars=10
).strip().upper()

if st.button("Analyze", type="primary", disabled=not ticker_symbol):
    if ticker_symbol:
        try:
            with st.spinner(f"Fetching financial data for {ticker_symbol}..."):
                df = calculate_ratios(ticker_symbol)
            
            st.success(f"✅ Analysis complete for {ticker_symbol}")
            
            # Display results
            st.subheader("Financial Ratios")
            st.dataframe(
                df.style.format({
                    "2025": "{:.4f}",
                    "2024": "{:.4f}",
                    "YoY Change": "{:.4f}"
                }),
                use_container_width=True,
                hide_index=True
            )
            
        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.info("This ticker may not have sufficient financial data available.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please verify the ticker symbol and try again.")
    else:
        st.warning("⚠️ Please enter a ticker symbol")