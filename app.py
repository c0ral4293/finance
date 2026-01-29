import streamlit as st
import time
from ratios import calculate_all_ratios

st.title("Financial Ratio Analyzer")

ticker = st.text_input("Enter ticker (AAPL, MSFT, TSLA)")

if ticker:
    st.write("Starting calculation...")
    time.sleep(0.2)

    try:
        st.write("Calling backend...")
        df = calculate_all_ratios(ticker.upper())
        st.success("Data fetched")
        st.dataframe(df)

    except Exception as e:
        st.error("Backend failed")
        st.exception(e)