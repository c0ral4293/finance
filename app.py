import streamlit as st
from ratios import calculate_ratios

st.set_page_config(page_title="Financial Ratios", page_icon="📊")

st.title("📊 Financial Ratios Analyzer")

ticker_symbol = st.text_input(
    "Enter Stock Ticker Symbol",
    value="AAPL"
)

if st.button("Analyze"):
    try:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            df = calculate_ratios(ticker_symbol)
        
        st.success(f"✅ Analysis complete for {ticker_symbol}")
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")